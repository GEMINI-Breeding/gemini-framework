from typing import Any, ClassVar
from enum import Enum
from gemini.pipeline.container_manager import GEMINIContainerManager
from gemini.config.settings import GEMINISettings

from pydantic import BaseModel, ConfigDict, PrivateAttr, Field

class GEMINIStatus(Enum):
    STOPPED = "STOPPED"
    BUILDING = "BUILDING"
    RUNNING = "RUNNING"
    CLEANING = "CLEANING"


class GEMINIManager(BaseModel):

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    _shared_state: ClassVar[dict] = PrivateAttr(default={})

    container_manager: GEMINIContainerManager = GEMINIContainerManager()
    settings: GEMINISettings = GEMINISettings()
    status: GEMINIStatus = GEMINIStatus.STOPPED

    def model_post_init(self, __context: Any) -> None:
        return super().model_post_init(__context)

    def apply_settings(self, settings: GEMINISettings) -> None:
        self.container_manager.apply_settings(settings)
        self.settings = settings

    def build_pipeline(self) -> bool:
        self.status = GEMINIStatus.BUILDING
        return self.container_manager.build_images()
    
    def start_pipeline(self) -> bool:
        self.status = GEMINIStatus.RUNNING
        return self.container_manager.start_containers()
    
    def stop_pipeline(self) -> bool:
        self.status = GEMINIStatus.STOPPED
        return self.container_manager.stop_containers()
    
    def clean_pipeline(self) -> bool:
        self.status = GEMINIStatus.CLEANING
        return self.container_manager.purge_containers()
