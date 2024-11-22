from typing import Any
from pydantic import BaseModel
from enum import Enum
from abc import ABC, abstractmethod

from gemini.config.settings import GEMINISettings
from gemini.pipeline.container_manager import GEMINIContainerManager

class GEMINIPipelineStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class GEMINIPipelineType(str, Enum):
    NONE = "none"
    DOCKER = "docker"
    KUBERNETES = "kubernetes"

class GEMINIPipeline(BaseModel):

    pipeline_settings : GEMINISettings
    pipeline_status : GEMINIPipelineStatus
    pipeline_type : GEMINIPipelineType

    @abstractmethod
    def start_pipeline(self) -> bool:
        pass

    @abstractmethod
    def stop_pipeline(self) -> bool:
        pass

    @abstractmethod
    def clean_pipeline(self) -> bool:
        pass

class GEMINIDockerPipeline(GEMINIPipeline):

    pipeline_type: GEMINIPipelineType = GEMINIPipelineType.DOCKER

    container_manager: GEMINIContainerManager = GEMINIContainerManager()

    def model_post_init(self, __context: Any) -> None:

        # Set the container manager
        self.container_manager = GEMINIContainerManager(pipeline_settings=self.pipeline_settings)

        return super().model_post_init(__context)

    def start_pipeline(self) -> bool:
        try:
            self.container_manager.setup()
            return True
        except Exception as e:
            print(e)
            return False

    def stop_pipeline(self) -> bool:
        try:
            self.container_manager.stop()
            return True
        except Exception as e:
            print(e)
            return False

    def clean_pipeline(self) -> bool:
        try:
            self.container_manager.teardown()
            return True
        except Exception as e:
            print(e)
            return False

