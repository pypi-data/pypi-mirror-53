# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Proxy Class for communication with Jasmine Orchestration Service, which wraps JasmineClient operations."""
from typing import cast, Dict, Any, Optional, List
import logging

from azureml._restclient.jasmine_client import JasmineClient
from azureml._restclient.models.feature_config_request import FeatureConfigRequest
from azureml._restclient.models.feature_config_response import FeatureConfigResponse
from azureml._restclient.models.feature_profile_input_dto import FeatureProfileInputDto
from azureml._restclient.models.feature_profile_output_dto import FeatureProfileOutputDto

from azureml.automl.core.abstract_jasmine_client import AbstractJasmineClient
from azureml.automl.core.configuration.sweeper_config import SweeperConfig
from azureml.automl.core.automl_datamodel_utilities import get_feature_sweeping_config_request


class JasmineClientProxy(AbstractJasmineClient):
    """Wrapper class for jasmine client operations."""

    def __init__(self, jasmine_client: JasmineClient, logger: Optional[logging.Logger] = None):
        """
        Create jasmine rest client wrapper.

        :param jasmine_client: Jasmine REST client.
        :param logger: Logger.
        """
        self.jasmine_client = jasmine_client
        self._logger = logger or logging.getLogger(JasmineClientProxy.__class__.__name__)
        self.feature_profile_input_dto_version = "1.0.0"

    def _get_feature_profiles(self, parent_run_id: str,
                              feature_config_requests: List[FeatureConfigRequest]) -> \
            Dict[str, FeatureConfigResponse]:
        """
        Get feature profile information for specified list of features.

        :param run_id: Parent run id.
        :param feature_config_requests: List of FeatureConfigRequest object.
        :rtype: Dict[str, FeatureConfigResponse] where key is feature_id.
        """
        input_map = {}  # type: Dict[str, FeatureConfigRequest]
        for feature in feature_config_requests:
            input_map[feature.feature_id] = feature
        feature_profile_input_dto = FeatureProfileInputDto(version=self.feature_profile_input_dto_version,
                                                           feature_config_input_map=input_map)
        response_dto = self.jasmine_client.get_feature_profiles(
            parent_run_id, feature_profile_input_dto)  # type: FeatureProfileOutputDto
        return cast(Dict[str, FeatureConfigResponse], response_dto.feature_config_output_map)

    def get_feature_sweeping_config(self, parent_run_id: str, task_type: str, is_gpu: bool = False) -> Dict[str, Any]:
        """
        Get feature sweeping config from JOS.

        :param parent_run_id: AutoML parent run Id.
        :param task_type: Task type- Classification, Regression, Forecasting.
        :param is_gpu: If machine is gpu enabled.
        :rtype: Feature sweeping config for the specified task type, empty if not available/found.
        """
        try:
            feature_config_request = get_feature_sweeping_config_request(task_type=task_type,
                                                                         is_gpu=is_gpu)
            response = self._get_feature_profiles(parent_run_id,
                                                  [feature_config_request])  # type: FeatureProfileOutputDto

            feature_conf_response = response[feature_config_request.feature_id]  # type: FeatureConfigResponse

            feature_sweeping_config = response[feature_config_request.feature_id].feature_config_map['config'] \
                if feature_conf_response.is_enabled else {}
            return cast(Dict[str, Any], feature_sweeping_config)
        except Exception as e:
            # Putting below message as info to avoid notebook failure due to warning.
            message = "Unable to fetch feature sweeping config from service, defaulting to blob store config."
            self._logger.info("{message}".format(message=message))
            # Below code can be used to test the feature_sweeping_config changes locally or on remote machine without
            # need of JOS.
            config = self._get_config()
            return cast(Dict[str, Any], config[task_type])

    def _get_config(self) -> Dict[str, Any]:
        """Read config and setup the list of enabled sweepers."""
        try:
            return SweeperConfig(logger=self._logger).get_config()
        except (IOError, FileNotFoundError) as e:
            self._logger.warning("Error trying to read configuration file: {e}".format(e=e))
            return {}
