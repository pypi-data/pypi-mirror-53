# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import ctypes
import warnings
import platform
import datetime
import sys
import io
import os
import csv
import json
import atexit
import signal
import copy
import uuid
import time

try:
    import flask
    from flask import request
except ImportError:
    pass
try:
    from pyspark.sql import DataFrame
except ImportError:
    pass
try:
    import pandas as pd
except ImportError:
    pass
try:
    import numpy as np
except ImportError:
    pass

__doc__ = '''\
ModelDataCollector is used to track input going into models, saving it in Azure Storage for further analysis.
'''

class std_tm(ctypes.Structure):
    _fields_ = [
        ("tm_sec", ctypes.c_int),
        ("tm_min", ctypes.c_int),
        ("tm_hour", ctypes.c_int),
        ("tm_mday", ctypes.c_int),
        ("tm_mon", ctypes.c_int),
        ("tm_year", ctypes.c_int),
        ("tm_wday", ctypes.c_int),
        ("tm_yday", ctypes.c_int),
        ("tm_isdst", ctypes.c_int),
    ]

class ModelDataCollector(object):
    '''
    A class that manages the collection and storage of input data provided to models and the corresponding predictions.

    When model data collection is enabled, data will be sent to the following container path:
    /modeldata/{workspace}/{webservice_name}/{model_name}/{model_version}/{designation}/{year}/{month}/{day}/{collection_name}.csv
    '''
    AML_DC_CORRELATION_HEADER = '$aml_dc_correlation_id'
    AML_DC_SCORING_TIMESTAMP_HEADER = '$aml_dc_scoring_timestamp'
    AML_DC_BOUNDARY_HEADER = '$aml_dc_boundary'
    AML_WORKSPACE_HEADER = '$aml_workspace'
    AML_SERVICE_NAME_HEADER = '$aml_service_name'
    AML_MODEL_NAME_HEADER = '$aml_model_name'
    AML_MODEL_VERSION_HEADER = '$aml_model_version'
    AML_REQUEST_ID_HEADER = '$aml_request_id'

    if platform.system() == "Windows":
        dllpath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'tools', 'modeldatacollector',
            'lib', 'native', 'Windows')
        os.environ['PATH'] = dllpath + ';' + os.environ['PATH']
        _lib = ctypes.CDLL('modeldatacollector.dll', use_last_error=True)
    elif platform.system() == "Darwin":
        libmodeldatacollector = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'tools', 'modeldatacollector', 'lib',
            'native', 'Darwin', 'libmodeldatacollector.dylib')
        _lib = ctypes.CDLL(libmodeldatacollector, use_last_error=True)
    else:
        libmodeldatacollector = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                             'tools', 'modeldatacollector', 'lib',
                                             'native', 'Linux', 'libmodeldatacollector.so')
        _lib = ctypes.CDLL(libmodeldatacollector, use_last_error=True)

    def __init__(self, model_name, designation='default',
                 feature_names=None, workspace='default/default/default',
                 webservice_name='default', model_version='default',
                 collection_name='default'):
        """
        Instantiates a new ModelDataCollector.

        When model data collection is enabled, data will be sent to the following container path:
        /modeldata/{workspace}/{webservice_name}/{model_name}/{model_version}/{designation}/{year}/{month}/{day}/{collection_name}.csv

        :param model_name: The name of the model which data is being collected for
        :type model_name: str
        :param designation: A unique designation for the data collection location. Supported designations: 'inputs', 'predictions', 'labels', 'signals, 'general'
        :type designation: str
        :param feature_names: A list of feature names that become the csv header when supplied
        :type feature_names: list
        :param workspace: The identifier for the AML workspace in the form subscriptionId/resourceGroup/workspaceName. This is populated automatically when models are operationalized through AML.
        :type workspace: str
        :param webservice_name: The name of the webservice to which this model is currently deployed. This is populated automatically when models are operationalized through AML.
        :type webservice_name: str
        :param model_version: The version of the model. This is populated automatically when models are operationalized through AML.
        :type model_version: str
        :return: An instance of a ModelDataCollector
        :rtype: ModelDataCollector
        """
        self._init_c_functions()

        if 'flask' in sys.modules:
            self._aml_operationalization = True
        else:
            self._aml_operationalization = False

        self._cloud_enabled = ModelDataCollector._lib.IsDataCollectionEnabled()

        self._debug = False
        
        self._feature_names = copy.copy(feature_names)
        self._correlation_headers = [] # set this on inputs or add_correlations

        if os.environ.get('AML_MODEL_DC_DEBUG') and os.environ.get('AML_MODEL_DC_DEBUG').lower() == 'true':
            self._debug = True
            print("Data collection is in debug mode. " +
                  "Set environment variable AML_MODEL_DC_STORAGE_ENABLED to 'true' " +
                  "to send data to the cloud (http://aka.ms/amlmodeldatacollection).")
        elif not self._cloud_enabled:
            print("Data collection is not enabled. " +
                  "Set environment variable AML_MODEL_DC_STORAGE_ENABLED to 'true' " +
                  "to enable (http://aka.ms/amlmodeldatacollection).")
            return

        if designation == 'default':
            self._designation = 'general'
        elif designation in ['inputs', 'predictions', 'labels', 'signals', 'general']:
            self._designation = designation
        else:
            print("Incorrect designation value. " +
                  "Supported values: 'default', 'inputs', 'predictions', 'labels', 'signals', 'general'")
            return

        self.workspace = workspace.lower()
        self.workspace_name = 'default'
        self.model_name = model_name
        self.model_version = model_version
        self.model_internal_id = ''
        self.workspace_internal_id = ''
        self.service_name = webservice_name
        self.service_internal_id = ''
        self.compute_name = ''
        self.compute_type = ''
        self.compute_location = ''
        self.aml_dc_hour_boundary = False
        self.model_config_map = None
        self.data_collector_storage_path = ''

        # update settings from the config_map file if available and from env variables
        self._load_config_map_and_env_settings()

        self._handle = -1
        self._correlation_handles = []
        self._current_correlation_handle_data = None
        self._current_correlation_handle = -1
        self._correlation_handle_creation_time = time.time()
        self.filename = '{}.csv'.format(collection_name)

        designation_with_expected_correlations = ['predictions', 'labels', 'signals']
        self._collect_for_correlation = self._designation in designation_with_expected_correlations

        if self._cloud_enabled:
            # Initialize TrackR and save handle
            str_model_version = str(self.model_version)
            if sys.version_info[0] < 3:
                self._handle = ModelDataCollector._lib.Init(
                    self.workspace, self.workspace_internal_id, self.service_name,
                    self.service_internal_id, self.model_name, str_model_version,
                    self.model_internal_id, self.compute_name, self.compute_type,
                    self.compute_location,self._designation, self.data_collector_storage_path,
                    self.filename)
            else:
                self._handle = ModelDataCollector._lib.InitW(
                    self.workspace, self.workspace_internal_id, self.service_name,
                    self.service_internal_id, self.model_name, str_model_version,
                    self.model_internal_id, self.compute_name, self.compute_type,
                    self.compute_location, self._designation, self.data_collector_storage_path,
                    self.filename)

            if self._handle == -1:
                warnings.warn("initialize failed: environment variable AML_MODEL_DC_STORAGE" +
                                "must be set to an Azure storage connection string " +
                                "(http://aka.ms/amlmodeldatacollection).")
                return

        if self._designation == 'inputs':
            self._add_correlation_headers()
        self._write_default_headers(self._handle)
        
        # For performance reasons, we write headears on all collect calls
        # So, keeping a flag to know if we already updated the headers based on the collected data
        # this only matters for the pandas and spark cases
        self.headersUpdated = False

        signal.signal(signal.SIGTERM, self._sigterm_handler)

    def _init_c_functions(self):
        # Shutdown
        ModelDataCollector._lib.Shutdown.argtypes = [ctypes.c_int]

        # InitW
        ModelDataCollector._lib.InitW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p,
            ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p,
            ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p,
            ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p]
        ModelDataCollector._lib.InitW.restype = ctypes.c_int

        # Init
        ModelDataCollector._lib.Init.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
            ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
            ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
            ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        ModelDataCollector._lib.Init.restype = ctypes.c_int

        # HandleForCorrelation
        ModelDataCollector._lib.HandleForCorrelation.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
                        ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, std_tm, ctypes.c_int]
        ModelDataCollector._lib.HandleForCorrelation.restype = ctypes.c_int

        # HandleForCorrelationW
        ModelDataCollector._lib.HandleForCorrelationW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p,
                        ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, std_tm, ctypes.c_int]
        ModelDataCollector._lib.HandleForCorrelationW.restype = ctypes.c_int

        # Shutdown
        ModelDataCollector._lib.Shutdown.argtypes = [ctypes.c_int]
        ModelDataCollector._lib.Shutdown.restype = ctypes.c_int

        # GetEventFlushIntervalTime
        ModelDataCollector._lib.GetEventFlushIntervalTime.argtypes = [ctypes.c_int]
        ModelDataCollector._lib.GetEventFlushIntervalTime.restype = ctypes.c_int

        # GetEventMaxQueueSize
        ModelDataCollector._lib.GetEventMaxQueueSize.argtypes = [ctypes.c_int]
        ModelDataCollector._lib.GetEventMaxQueueSize.restype = ctypes.c_int
        
        # GetEventRetryTime
        ModelDataCollector._lib.GetEventRetryTime.argtypes = [ctypes.c_int]
        ModelDataCollector._lib.GetEventRetryTime.restype = ctypes.c_int

        # IsDataCollectionEnabled
        ModelDataCollector._lib.IsDataCollectionEnabled.restype = ctypes.c_bool

    @atexit.register
    def _shutdown():
        ModelDataCollector._lib.ShutdownAll()

    def _uninit(self):
        ModelDataCollector._lib.ShutdownAll()

    def _sigterm_handler(self, signum, frame):
        print("Model data collection shutting down: SIGTERM called")
        ModelDataCollector._lib.ShutdownAll()
        sys.exit(0)

    def _shutdown_handle(self, handle):
        ModelDataCollector._lib.Shutdown(handle)

    def _load_config_map_and_env_settings(self):
        if os.path.isfile("/var/azureml-app/model_config_map.json"):
            with open("/var/azureml-app/model_config_map.json") as config_map_json:
                self.model_config_map = json.load(config_map_json)

        model_storage_path = ''

        if not self.model_config_map == None:
            if 'modelsInfo' in self.model_config_map and self.model_name in self.model_config_map['modelsInfo']:
                model_versions = list(self.model_config_map['modelsInfo'][self.model_name])
                if self.model_version == 'default' and len(model_versions) > 0:
                    model_versions = list(self.model_config_map['modelsInfo'][self.model_name])
                    model_versions.sort(key=lambda x: int(x))
                    self.model_version = model_versions[-1]
                if 'internalId' in self.model_config_map['modelsInfo'][self.model_name][self.model_version]:
                    self.model_internal_id = self.model_config_map['modelsInfo'][self.model_name][self.model_version]['internalId']
                if 'dataCollectorStoragePath' in self.model_config_map['modelsInfo'][self.model_name][self.model_version]:
                    model_storage_path = self.model_config_map['modelsInfo'][self.model_name][self.model_version]['dataCollectorStoragePath']
            if self.workspace == 'default/default/default':
                if 'accountContext' in self.model_config_map:
                    if 'subscriptionId' in self.model_config_map['accountContext'] and \
                            'resourceGroupName' in self.model_config_map['accountContext'] and \
                            'accountName' in self.model_config_map['accountContext']:
                        subscription_id = self.model_config_map['accountContext']['subscriptionId'].lower()
                        resource_group_name = self.model_config_map['accountContext']['resourceGroupName'].lower()
                        self.workspace_name = self.model_config_map['accountContext']['accountName'].lower()
                        self.workspace = '{}/{}/{}'.format(subscription_id, resource_group_name, self.workspace_name)
                    if 'workspaceId' in self.model_config_map['accountContext']:
                        self.workspace_internal_id = self.model_config_map['accountContext']['workspaceId']

        if self.service_name == 'default' and os.environ.get('SERVICE_NAME'):
            self.service_name = os.environ.get('SERVICE_NAME')
        if os.environ.get('SERVICE_ID'):
            self.service_internal_id = os.environ.get('SERVICE_ID')
        if os.environ.get('COMPUTE_NAME'):
            self.compute_name = os.environ.get('COMPUTE_NAME')
        if os.environ.get('COMPUTE_TYPE'):
            self.compute_type = os.environ.get('COMPUTE_TYPE')
        if os.environ.get('COMPUTE_LOCATION'):
            self.compute_location = os.environ.get('COMPUTE_LOCATION')

        self.data_collector_storage_path = self._model_storage_path_for_service(model_storage_path, self.service_name)

        if os.environ.get("AML_MODEL_DC_BOUNDARY") and os.environ.get("AML_MODEL_DC_BOUNDARY") == 'hour':
            self.aml_dc_hour_boundary = True

    def _model_storage_path_for_service(self, model_storage_path, service_name):
        return model_storage_path.replace("{webservice_name}", service_name)

    def _write_default_headers(self, handle, data=None):
        if handle == -1:
            return
        csv_header_buffer = None
        # First see if we can extract headers from collection data
        if data is not None:
            if 'pandas' in sys.modules and isinstance(data, pd.DataFrame):
                csv_header_buffer = self._convert_list_to_csv_buffer(list(data))
            elif ('pyspark' in sys.modules and 'pandas' in sys.modules) and isinstance(data, DataFrame):
                csv_header_buffer = self._convert_list_to_csv_buffer(data.columns)
            elif self._feature_names is not None and self._cloud_enabled:
                csv_header_buffer = self._convert_list_to_csv_buffer(self._get_data_headers())
        elif self._feature_names is not None and self._cloud_enabled:
            csv_header_buffer = self._convert_list_to_csv_buffer(self._get_data_headers())

        if self._cloud_enabled and csv_header_buffer is not None:
            ModelDataCollector._lib.WriteHeader(handle, csv_header_buffer, len(csv_header_buffer))

    def collect(self, input_data, user_correlation_id=""):
        """
        Collect data for this ModelDataCollector instance.

        :param input_data: The data to be collected. For dataframe types, if a header exists with feature names, this information is included in the data destination without needing to explicitly pass feature names in the ModelDataCollector constructor.
        :type input_data: list, numpy.array, pandas.DataFrame, pyspark.sql.DataFrame
        :param user_correlation_id: An optional correlation id provided by the user to correlate this prediction
        :type user_correlation_id: str
        """
        if (not self._cloud_enabled or self._handle == -1) and not self._debug:
            return

        correlation_data = None
        if self._designation == 'inputs':
            correlation_data = self._get_generated_data_fields(user_correlation_id)
            input_data = self.add_correlations(input_data, correlation_data)

        if isinstance(input_data, list):
            if self._collect_for_correlation:
                return self._collect_list_for_correlation(input_data)
            csv_data_buffer = self._convert_list_to_csv(input_data)
            csv_header_buffer = None
        elif ('numpy' in sys.modules and 'pandas' in sys.modules) and isinstance(input_data, np.ndarray):
            if self._collect_for_correlation:
                return self._collect_numpy_for_correlation(input_data)
            csv_data_buffer = self._convert_numpy_to_csv_buffer(input_data)
            csv_header_buffer = None
        elif 'pandas' in sys.modules and isinstance(input_data, pd.DataFrame):
            if self._collect_for_correlation:
                return self._collect_pandas_for_correlation(input_data)
            csv_header_buffer, csv_data_buffer = self._convert_pandas_df_to_csv(input_data)
            if self._cloud_enabled and csv_header_buffer is not None and not self.headersUpdated:
                ModelDataCollector._lib.WriteHeader(self._handle, csv_header_buffer, len(csv_header_buffer))
                self.headersUpdated = True
        elif ('pyspark' in sys.modules and 'pandas' in sys.modules) and isinstance(input_data, DataFrame):
            if self._collect_for_correlation:
                return self._collect_pyspark_for_correlation(input_data)
            csv_header_buffer, csv_data_buffer = self._convert_spark_df_to_csv(input_data)
            if self._cloud_enabled and csv_header_buffer is not None and not self.headersUpdated:
                ModelDataCollector._lib.WriteHeader(self._handle, csv_header_buffer, len(csv_header_buffer))
                self.headersUpdated = True
        else:
            warnings.warn('collect failed: input data must be list,' +
                          'numpy array, pandas dataframe, or spark dataframe. ' +
                          'Corresponding modules must be installed first.')
            return None

        if self._cloud_enabled:
            self._handle = ModelDataCollector._lib.WriteBinary(self._handle, csv_data_buffer, len(csv_data_buffer))
        if self._debug:
            self._write_to_stdout(csv_header_buffer, csv_data_buffer)

        return correlation_data

    def add_correlations(self, input_data, correlations):
        if correlations is None:
            return input_data
        self._add_correlation_headers()
        if isinstance(input_data, list):
            return self._add_correlation_data_to_list(input_data, correlations)
        elif ('numpy' in sys.modules and 'pandas' in sys.modules) and isinstance(input_data, np.ndarray):
            if input_data.ndim == 1:
                # Transposing so that data is a single row not single column
                input_data = np.array([input_data])

            # there is a performace hit on converting to pandas_df, so
            # doing this directly on numpy
            return self._add_correlation_data_to_numpy(input_data, correlations)
        elif 'pandas' in sys.modules and isinstance(input_data, pd.DataFrame):
            return self._add_correlation_data_to_pandas(input_data, correlations)
        elif ('pyspark' in sys.modules and 'pandas' in sys.modules) and isinstance(input_data, DataFrame):
            pandas_df = input_data.toPandas()
            augmented_df = self._add_correlation_data_to_pandas(pandas_df, correlations)
            return augmented_df

        else:
            warnings.warn('collect failed: input data must be list,' +
                          'numpy array, pandas dataframe, or spark dataframe. ' +
                          'Corresponding modules must be installed first.')
            return input_data

    def _getEventFlushIntervalTime(self):
        return ModelDataCollector._lib.GetEventFlushIntervalTime(self._handle)
        
    def _getEventMaxQueueSize(self):
        return ModelDataCollector._lib.GetEventMaxQueueSize(self._handle)

    def _getEventRetryTime(self):
        return ModelDataCollector._lib.GetEventRetryTime(self._handle)

    def _get_data_headers(self):
        return  self._feature_names + self._correlation_headers if self._correlation_headers else self._feature_names

    def _add_correlation_headers(self):
        if not self._correlation_headers:
            self._correlation_headers = [
                ModelDataCollector.AML_DC_CORRELATION_HEADER, 
                ModelDataCollector.AML_DC_SCORING_TIMESTAMP_HEADER,
                ModelDataCollector.AML_DC_BOUNDARY_HEADER,
                ModelDataCollector.AML_WORKSPACE_HEADER,
                ModelDataCollector.AML_SERVICE_NAME_HEADER,
                ModelDataCollector.AML_MODEL_NAME_HEADER,
                ModelDataCollector.AML_MODEL_VERSION_HEADER,
                ModelDataCollector.AML_REQUEST_ID_HEADER]

    def _get_generated_data_fields(self, correlation_id=''):
        timestamp = datetime.datetime.utcnow().isoformat()
        correlation = str(uuid.uuid4())
        request_id = '00000000-0000-0000-0000-000000000000'

        if self._aml_operationalization and flask.has_request_context():
            if 'REQUEST_ID' in request.environ:
                request_id = request.environ['REQUEST_ID']

        generated_id = '{}-{}'.format(correlation_id, correlation) if correlation_id != '' else correlation

        # Not running in AML context with flask/request id
        return {
            ModelDataCollector.AML_DC_SCORING_TIMESTAMP_HEADER: timestamp,
            ModelDataCollector.AML_REQUEST_ID_HEADER: request_id,
            ModelDataCollector.AML_DC_CORRELATION_HEADER: generated_id,
            ModelDataCollector.AML_DC_BOUNDARY_HEADER: 60 if self.aml_dc_hour_boundary else 60*24,
            ModelDataCollector.AML_WORKSPACE_HEADER: self.workspace,
            ModelDataCollector.AML_SERVICE_NAME_HEADER: self.service_name,
            ModelDataCollector.AML_MODEL_NAME_HEADER: self.model_name,
            ModelDataCollector.AML_MODEL_VERSION_HEADER: self.model_version}

    def _write_to_stdout(self, header_buffer, data_buffer):
        if not header_buffer:
            if self._feature_names:
                header_buffer = self._convert_list_to_csv_buffer(self._get_data_headers())

        if header_buffer:
            if isinstance(header_buffer, str):
                print(header_buffer + data_buffer)
            elif isinstance(header_buffer, bytes) or isinstance(header_buffer, bytearray):
                print(header_buffer.decode() + data_buffer.decode())
        else:
            if isinstance(data_buffer, str):
                print(data_buffer)
            elif isinstance(data_buffer, bytes) or isinstance(data_buffer, bytearray):
                print(data_buffer.decode())

    def _convert_list_to_csv(self, input_list):
        buffer_object = self._convert_list_to_csv_buffer(input_list)
        return buffer_object

    def _convert_numpy_to_csv_buffer(self, numpy_data):
        if numpy_data.ndim == 1:
            # Transposing so that data is a single row not single column
            numpy_data = [numpy_data]

        if sys.version_info[0] < 3:
            buf = io.BytesIO()
            csvwriter = csv.writer(buf)
            csvwriter.writerows(numpy_data)
        else:
            stringbuf = io.StringIO()
            csvwriter = csv.writer(stringbuf)
            csvwriter.writerows(numpy_data)
            buf = io.BytesIO(stringbuf.getvalue().encode())

        return buf.getvalue()

    def _convert_pandas_df_to_csv(self, user_pandas_df):
        header_buffer, data_buffer = self._convert_pandas_df_to_csv_buffers(user_pandas_df)
        return header_buffer, data_buffer

    def _convert_spark_df_to_csv(self, spark_df):
        # Use pandas conversion
        pandas_df = spark_df.toPandas()
        header_buffer, data_buffer = self._convert_pandas_df_to_csv(pandas_df)
        return header_buffer, data_buffer

    def _convert_list_to_csv_buffer(self, input_list):
        # csvwriter in python 2 and 3 requires a different type of buffer due to string encoding differences
        if sys.version_info[0] < 3:
            buf = io.BytesIO()
            csvwriter = csv.writer(buf)
            csvwriter.writerow(input_list)
        else:
            stringbuf = io.StringIO()
            csvwriter = csv.writer(stringbuf)
            csvwriter.writerow(input_list)
            buf = io.BytesIO(stringbuf.getvalue().encode())

        return buf.getvalue()

    def _convert_pandas_df_to_csv_buffers(self, pandas_df):
        # Puts the header names into a buffer
        header_buf = self._convert_list_to_csv_buffer(list(pandas_df))
        if sys.version_info[0] < 3:
            buf = io.BytesIO()
            pandas_df.to_csv(buf, index=False, header=False)
            return header_buf, buf.getvalue()
        else:
            stringbuf = io.StringIO()
            pandas_df.to_csv(stringbuf, index=False, header=False)
            buf = io.BytesIO(stringbuf.getvalue().encode())
            return header_buf, buf.getvalue()

    def _add_correlation_data_to_list(self, input_data, correlation_data):
        return input_data + [correlation_data[ModelDataCollector.AML_DC_CORRELATION_HEADER],
            correlation_data[ModelDataCollector.AML_DC_SCORING_TIMESTAMP_HEADER],
            correlation_data[ModelDataCollector.AML_DC_BOUNDARY_HEADER],
            correlation_data[ModelDataCollector.AML_WORKSPACE_HEADER],
            correlation_data[ModelDataCollector.AML_SERVICE_NAME_HEADER],
            correlation_data[ModelDataCollector.AML_MODEL_NAME_HEADER],
            correlation_data[ModelDataCollector.AML_MODEL_VERSION_HEADER],
            correlation_data[ModelDataCollector.AML_REQUEST_ID_HEADER]]

    def _add_correlation_data_to_numpy(self, input_data, correlation_data):
        correlation = np.array([[correlation_data[ModelDataCollector.AML_DC_CORRELATION_HEADER],
            correlation_data[ModelDataCollector.AML_DC_SCORING_TIMESTAMP_HEADER],
            correlation_data[ModelDataCollector.AML_DC_BOUNDARY_HEADER],
            correlation_data[ModelDataCollector.AML_WORKSPACE_HEADER],
            correlation_data[ModelDataCollector.AML_SERVICE_NAME_HEADER],
            correlation_data[ModelDataCollector.AML_MODEL_NAME_HEADER],
            correlation_data[ModelDataCollector.AML_MODEL_VERSION_HEADER],
            correlation_data[ModelDataCollector.AML_REQUEST_ID_HEADER]]], dtype=object)
            
        # We need to match rows with input data
        rows = input_data.shape[0]
        correlation_array = np.repeat(correlation, rows, axis=0)
        return np.append(input_data, correlation_array, axis=1)

    def _add_correlation_data_to_pandas(self, input_data, correlation_data):
        pandas_df = input_data.copy(deep=False)
        current_last = len(pandas_df.columns)
        pandas_df.insert(current_last, ModelDataCollector.AML_DC_CORRELATION_HEADER, correlation_data[ModelDataCollector.AML_DC_CORRELATION_HEADER])
        pandas_df.insert(current_last + 1, ModelDataCollector.AML_DC_SCORING_TIMESTAMP_HEADER, correlation_data[ModelDataCollector.AML_DC_SCORING_TIMESTAMP_HEADER])
        pandas_df.insert(current_last + 2, ModelDataCollector.AML_DC_BOUNDARY_HEADER, correlation_data[ModelDataCollector.AML_DC_BOUNDARY_HEADER])
        pandas_df.insert(current_last + 3, ModelDataCollector.AML_WORKSPACE_HEADER, correlation_data[ModelDataCollector.AML_WORKSPACE_HEADER])
        pandas_df.insert(current_last + 4, ModelDataCollector.AML_SERVICE_NAME_HEADER, correlation_data[ModelDataCollector.AML_SERVICE_NAME_HEADER])
        pandas_df.insert(current_last + 5, ModelDataCollector.AML_MODEL_NAME_HEADER, correlation_data[ModelDataCollector.AML_MODEL_NAME_HEADER])
        pandas_df.insert(current_last + 6, ModelDataCollector.AML_MODEL_VERSION_HEADER, correlation_data[ModelDataCollector.AML_MODEL_VERSION_HEADER])
        pandas_df.insert(current_last + 7, ModelDataCollector.AML_REQUEST_ID_HEADER, correlation_data[ModelDataCollector.AML_REQUEST_ID_HEADER])
        return pandas_df

    def _get_std_tm_from_time_tm(self, tm):
        return std_tm(tm.tm_sec, tm.tm_min, tm.tm_hour, tm.tm_mday, tm.tm_mon-1, tm.tm_year-1900, tm.tm_wday, tm.tm_yday, tm.tm_isdst)

    def _get_handle_for_correlation(self, correlation_data, data=None):

        if self._need_new_handle(correlation_data):
            
            current_time = time.time()
            if current_time - self._correlation_handle_creation_time > 1:
                self._shutdown_current_correlation_handles()
            
            tm = self._get_std_tm_from_time_tm(correlation_data['tm'])
            storage_path = self._model_storage_path_from_config_map(correlation_data["model_name"], str(correlation_data["model_version"]), correlation_data["service_name"])
            handle = -1
            if self._cloud_enabled:
                # Initialize TrackR and save handle
                if sys.version_info[0] < 3:
                    handle = ModelDataCollector._lib.HandleForCorrelation(
                        correlation_data["workspace"], correlation_data["service_name"],
                        correlation_data["model_name"], str(correlation_data["model_version"]),
                        self._designation, storage_path, self.filename, tm, int(correlation_data["boundary"]))
                else:
                    handle = ModelDataCollector._lib.HandleForCorrelationW(
                        correlation_data["workspace"], correlation_data["service_name"],
                        correlation_data["model_name"], str(correlation_data["model_version"]),
                        self._designation, storage_path, self.filename, tm, int(correlation_data["boundary"]))

                if handle == -1:
                    warnings.warn("initialize failed: environment variable AML_MODEL_DC_STORAGE" +
                                "must be set to an Azure storage connection string " +
                                "(http://aka.ms/amlmodeldatacollection).")
            self._current_correlation_handle = handle
            self._current_correlation_handle_data = correlation_data
            self._correlation_handles.append(handle)
            self._correlation_handle_creation_time = time.time()
            self._write_default_headers(handle, data)
            return handle
        else:
            return self._current_correlation_handle

    def _need_new_handle(self, new_correlation_data):
        if self._current_correlation_handle == -1:
            return True
        
        if self._current_correlation_handle_data is None:
            return True

        if self._current_correlation_handle_data['workspace'] != new_correlation_data['workspace'] or \
            self._current_correlation_handle_data['service_name'] != new_correlation_data['service_name'] or \
            self._current_correlation_handle_data['model_name'] != new_correlation_data['model_name'] or \
            self._current_correlation_handle_data['model_version'] != new_correlation_data['model_version'] or \
            int(self._current_correlation_handle_data['boundary']) != int(new_correlation_data['boundary']):
            return True
        
        # this needs better logic
        if self._current_correlation_handle_data['tm'].tm_year != new_correlation_data['tm'].tm_year or \
            self._current_correlation_handle_data['tm'].tm_mon != new_correlation_data['tm'].tm_mon or \
            self._current_correlation_handle_data['tm'].tm_mday != new_correlation_data['tm'].tm_mday:
            return True

        if int(self._current_correlation_handle_data['boundary']) == 60:
            if self._current_correlation_handle_data['tm'].tm_hour != new_correlation_data['tm'].tm_hour:
                return True

        return False

    def _need_special_handle(self, headers):
        if ModelDataCollector.AML_DC_SCORING_TIMESTAMP_HEADER in headers or \
            ModelDataCollector.AML_WORKSPACE_HEADER in headers or \
            ModelDataCollector.AML_MODEL_NAME_HEADER in headers or \
            ModelDataCollector.AML_MODEL_VERSION_HEADER in headers or \
            ModelDataCollector.AML_SERVICE_NAME_HEADER in headers:
            return True
        
        return False

    def _collect_list_for_correlation(self, data):
        data_headers = []
        if self._feature_names:
            data_headers = self._get_data_headers()
        if self._need_special_handle(data_headers):
            handle_data = {}
            handle_data['workspace'] = data[data_headers.index(ModelDataCollector.AML_WORKSPACE_HEADER)] \
                if ModelDataCollector.AML_WORKSPACE_HEADER in data_headers and data_headers.index(ModelDataCollector.AML_WORKSPACE_HEADER) < len(data) \
                else self.workspace
            handle_data['service_name'] = data[data_headers.index(ModelDataCollector.AML_SERVICE_NAME_HEADER)] \
                if ModelDataCollector.AML_SERVICE_NAME_HEADER in data_headers and data_headers.index(ModelDataCollector.AML_SERVICE_NAME_HEADER) < len(data) \
                else self.service_name
            handle_data['model_name'] = data[data_headers.index(ModelDataCollector.AML_MODEL_NAME_HEADER)] \
                if ModelDataCollector.AML_MODEL_NAME_HEADER in data_headers and data_headers.index(ModelDataCollector.AML_MODEL_NAME_HEADER) < len(data) \
                else self.model_name
            handle_data['model_version'] = data[data_headers.index(ModelDataCollector.AML_MODEL_VERSION_HEADER)] \
                if ModelDataCollector.AML_MODEL_VERSION_HEADER in data_headers and data_headers.index(ModelDataCollector.AML_MODEL_VERSION_HEADER) < len(data) \
                else self.model_version
            handle_data['boundary'] = int(data[data_headers.index(ModelDataCollector.AML_DC_BOUNDARY_HEADER)]) \
                if ModelDataCollector.AML_DC_BOUNDARY_HEADER in data_headers and data_headers.index(ModelDataCollector.AML_DC_BOUNDARY_HEADER) < len(data) \
                else 60*24

            if ModelDataCollector.AML_DC_SCORING_TIMESTAMP_HEADER in data_headers and data_headers.index(ModelDataCollector.AML_DC_SCORING_TIMESTAMP_HEADER) < len(data):
                timestamp = data[data_headers.index(ModelDataCollector.AML_DC_SCORING_TIMESTAMP_HEADER)]
                try:
                        handle_data['tm'] = time.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
                except ValueError:
                    try:
                        handle_data['tm'] = time.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
                    except ValueError:
                        tm = time.gmtime()
            else:
                handle_data['tm'] = time.gmtime()

            correlation_handle = self._get_handle_for_correlation(handle_data)

            if self._cloud_enabled:
                csv_data_buffer = self._convert_list_to_csv(data)
                ModelDataCollector._lib.WriteBinaryBasic(correlation_handle, csv_data_buffer, len(csv_data_buffer))
        else:
            csv_data_buffer = self._convert_list_to_csv(data)
            if self._cloud_enabled:
                self._write_default_headers(self._handle, data)
                self._handle = ModelDataCollector._lib.WriteBinary(self._handle, csv_data_buffer, len(csv_data_buffer))

    def _collect_pandas_for_correlation(self, data):
        # TODO: checks and fallbacks
        if self._need_special_handle(data.columns):
            it = data.iterrows()
            for row_pair in it:
                tm = None
                if ModelDataCollector.AML_DC_SCORING_TIMESTAMP_HEADER in data.columns:
                    timestamp = row_pair[1][ModelDataCollector.AML_DC_SCORING_TIMESTAMP_HEADER]
                    try:
                        tm = time.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
                    except ValueError:
                        try:
                            tm = time.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
                        except ValueError:
                            tm = time.gmtime()
                else:
                    tm = time.gmtime()
                boundary = int(row_pair[1][ModelDataCollector.AML_DC_BOUNDARY_HEADER]) \
                    if ModelDataCollector.AML_DC_BOUNDARY_HEADER in data.columns \
                    else 60*24
                workspace = row_pair[1][ModelDataCollector.AML_WORKSPACE_HEADER] \
                    if ModelDataCollector.AML_WORKSPACE_HEADER in data.columns \
                    else self.workspace
                service_name = row_pair[1][ModelDataCollector.AML_SERVICE_NAME_HEADER] \
                    if ModelDataCollector.AML_SERVICE_NAME_HEADER in data.columns \
                    else self.service_name
                model_name = row_pair[1][ModelDataCollector.AML_MODEL_NAME_HEADER] \
                    if ModelDataCollector.AML_MODEL_NAME_HEADER in data.columns \
                    else self.model_name
                model_version = row_pair[1][ModelDataCollector.AML_MODEL_VERSION_HEADER] \
                    if ModelDataCollector.AML_MODEL_VERSION_HEADER in data.columns \
                    else self.model_version
                handle_data = {
                        'tm': tm,
                        'boundary': boundary,
                        'workspace': workspace,
                        'service_name': service_name,
                        'model_name': model_name,
                        'model_version': model_version
                    }

                current_handle = self._get_handle_for_correlation(handle_data, data)

                if self._cloud_enabled:
                    buffer = self._convert_list_to_csv_buffer(list(row_pair[1]))
                    ModelDataCollector._lib.WriteBinaryBasic(current_handle, buffer, len(buffer))
            
        else:
            csv_header_buffer, csv_data_buffer = self._convert_pandas_df_to_csv(data)
            if self._cloud_enabled:
                ModelDataCollector._lib.WriteHeader(self._handle, csv_header_buffer, len(csv_header_buffer))
                self._handle = ModelDataCollector._lib.WriteBinary(self._handle, csv_data_buffer, len(csv_data_buffer))

    def _collect_numpy_for_correlation(self, input_data):
        if input_data.ndim == 1:
            # Transposing so that data is a single row not single column
            input_data = np.array([input_data])

        for row in input_data:
            self._collect_list_for_correlation(row)
    
    def _collect_pyspark_for_correlation(self, input_data):
        pandas_df = input_data.toPandas()
        self._collect_pandas_for_correlation(pandas_df)

    def _model_storage_path_from_config_map(self, model_name, model_version, service_name):
        storage_path = ''
        if self.model_config_map is not None:
            if 'modelsInfo' in self.model_config_map and model_name in self.model_config_map['modelsInfo']:
                if 'dataCollectorStoragePath' in self.model_config_map['modelsInfo'][self.model_name][model_version]:
                    storage_path = self.model_config_map['modelsInfo'][self.model_name][model_version]['dataCollectorStoragePath']
        return self._model_storage_path_for_service(storage_path, service_name)

    def _shutdown_current_correlation_handles(self):
        for h in self._correlation_handles:
            self._shutdown_handle(h)
        self._correlation_handles = []
