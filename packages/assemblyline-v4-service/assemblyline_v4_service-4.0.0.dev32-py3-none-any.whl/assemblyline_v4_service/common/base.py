from __future__ import annotations

import logging
from typing import Optional, Dict, Any

from assemblyline.common import exceptions, log, version
from assemblyline.odm.messages.task import Task as ServiceTask
from assemblyline_v4_service.common import helper
from assemblyline_v4_service.common.request import ServiceRequest
from assemblyline_v4_service.common.task import Task


class ServiceBase:
    def __init__(self, config: Optional[Dict] = None) -> None:
        # Load the service attributes from the service manifest
        self.service_attributes = helper.get_service_attributes()

        # Start with default service parameters and override with anything provided
        self.config = self.service_attributes.config
        if config:
            self.config.update(config)

        # Initialize logging for the service
        log.init_logging(f'{self.service_attributes.name}', log_level=logging.INFO)
        self.log = logging.getLogger(f'assemblyline.service.{self.service_attributes.name.lower()}')

        self._task = None

        self._working_directory = None

    def _cleanup(self) -> None:
        self._task = None
        self._working_directory = None

    def _handle_execute_failure(self, exception, stack_info) -> None:
        # Clear the result, in case it caused the problem
        self._task.result = None

        # Clear the extracted and supplementary files
        self._task.clear_extracted()
        self._task.clear_supplementary()

        if isinstance(exception, exceptions.RecoverableError):
            self.log.info(f"Recoverable Service Error ({self._task.sid}/{self._task.sha256}) {exception}: {stack_info}")
            self._task.save_error(stack_info, recoverable=True)
        else:
            self.log.error(f"Nonrecoverable Service Error ({self._task.sid}/{self._task.sha256}) {exception}: {stack_info}")
            self._task.save_error(stack_info, recoverable=False)

    def _success(self) -> None:
        self._task.success()

    def execute(self, request: ServiceRequest) -> Dict[str, Any]:
        raise NotImplementedError("execute() function not implemented")

    def get_service_version(self) -> str:
        t = (version.FRAMEWORK_VERSION,
             version.SYSTEM_VERSION,
             self.service_attributes.version)
        return '.'.join([str(v) for v in t])

    def get_tool_version(self) -> Optional[str]:
        return None

    def handle_task(self, task: ServiceTask) -> None:
        try:
            self._task = Task(task)
            self.log.info(f"Starting task: {self._task.sid}/{self._task.sha256} ({self._task.type})")
            self._working_directory = self._task.working_directory()
            self._task.start(self.service_attributes.default_result_classification,
                             self.get_service_version(), self.get_tool_version())

            request = ServiceRequest(self._task)
            self.execute(request)

            result = self._task.result
            self._task.set_result(result)
            self._success()
        except Exception as ex:
            self._handle_execute_failure(ex, exceptions.get_stacktrace_info(ex))
        finally:
            self._cleanup()

    def start(self) -> None:
        """
        Called at worker start.

        :return:
        """
        pass

    def start_service(self) -> None:
        self.log.info(f"Starting service: {self.service_attributes.name}")
        self.start()

    def stop(self) -> None:
        """
        Called at worker stop.

        :return:
        """
        pass

    def stop_service(self) -> None:
        # Perform common stop routines and then invoke the child's stop().
        self.log.info(f"Stopping service: {self.service_attributes.name}")
        self.stop()
