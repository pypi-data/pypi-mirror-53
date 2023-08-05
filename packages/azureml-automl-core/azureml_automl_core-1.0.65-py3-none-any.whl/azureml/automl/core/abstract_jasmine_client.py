# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Abstract class for communication with Jasmine Orchestration Service."""
from typing import Any, List, Dict


class AbstractJasmineClient(object):
    """Abstract class representing jasmine client operations."""

    def __init__(self):
        """Class AbstractJasmineClient constructor.

        This is a base class and users should not be creating this class using the constructor.
        """
        pass

    def get_feature_sweeping_config(self, parent_run_id: str, task_type: str, is_gpu: bool) -> Dict[str, Any]:
        """
        Get feature sweeping config from. This method should not be called directly,
        concrete implementation of this class should do implementation.

        :param parent_run_id: AutoML parent run Id
        :param task_type: Task type- Classification, Regression, Forecasting
        :param is_gpu: If client machine has gpu visible to sdk and dependencies.
        :rtype: Feature sweeping config for the specified task type, empty if not available/found.
        """
        raise NotImplementedError()
