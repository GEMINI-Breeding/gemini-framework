from pydantic import BaseModel
from enum import Enum

from gemini.config.settings import GEMINISettings
from gemini.pipeline.container_manager import GEMINIContainerManager

class GEMINIPipelineStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class GEMINIPipelineType(str, Enum):
    DOCKER = "docker"
    KUBERNETES = "kubernetes"

class GEMINIPipeline(BaseModel):

    pipeline_settings: GEMINISettings = GEMINISettings()
    pipeline_status: GEMINIPipelineStatus = GEMINIPipelineStatus.PENDING
    pipeline_type: GEMINIPipelineType = GEMINIPipelineType.DOCKER

    container_manager: GEMINIContainerManager = None

    def start_pipeline(self) -> bool:
        try:
            if self.pipeline_type == GEMINIPipelineType.DOCKER:
                self.container_manager = GEMINIContainerManager(pipeline_settings=self.pipeline_settings)
                # Build the images
                self.container_manager.setup()

            elif self.pipeline_type == GEMINIPipelineType.KUBERNETES:
                # Start the kubernetes pipeline
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        
    def stop_pipeline(self) -> bool:
        try:
            if self.pipeline_type == GEMINIPipelineType.DOCKER:
                # Stop the containers
                self.container_manager.stop()
            elif self.pipeline_type == GEMINIPipelineType.KUBERNETES:
                # Stop the kubernetes pipeline
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        

    def clean_pipeline(self) -> bool:
        try:
            if self.pipeline_type == GEMINIPipelineType.DOCKER:
                # Purge the containers
                self.container_manager.teardown()
            elif self.pipeline_type == GEMINIPipelineType.KUBERNETES:
                # Clean the kubernetes pipeline
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False



