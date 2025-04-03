from typing import Any, ClassVar
from enum import Enum

from gemini.logger.interfaces import logger_provider
from gemini.storage.interfaces import storage_provider

from gemini.storage.providers.minio_storage import MinioStorageProvider
from gemini.logger.providers.redis_logger import RedisLogger

from gemini.pipeline.container_manager import GEMINIContainerManager
from gemini.config.settings import GEMINISettings

import git
from git import Repo, GitCommandError
import os

from pydantic import BaseModel, ConfigDict, PrivateAttr, Field

class GEMINIComponentType(str, Enum):
    LOGGER = "logger"
    STORAGE = "storage"
    DB = "db"



class GEMINIManager(BaseModel):

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    _shared_state: ClassVar[dict] = PrivateAttr(default={})

    container_manager: GEMINIContainerManager = GEMINIContainerManager()
    settings: GEMINISettings = GEMINISettings()

    def model_post_init(self, __context: Any) -> None:
        return super().model_post_init(__context)

    def apply_settings(self, settings: GEMINISettings) -> None:
        self.container_manager.apply_settings(settings)
        self.settings = settings

    def get_settings(self) -> GEMINISettings:
        return self.settings

    def build_pipeline(self) -> bool:
        return self.container_manager.build_images()
    
    def rebuild_pipeline(self) -> bool:
        return self.container_manager.rebuild_images()
    
    def start_pipeline(self) -> bool:
        return self.container_manager.start_containers()
    
    def stop_pipeline(self) -> bool:
        return self.container_manager.stop_containers()
    
    def clean_pipeline(self) -> bool:
        return self.container_manager.teardown()
    
    def get_status(self) -> str:
        return self.container_manager.get_status()
    
    def get_component_provider(self, component_type: GEMINIComponentType):
        component_settings = self._get_component_settings(component_type)
        if component_type == GEMINIComponentType.LOGGER:
            return RedisLogger(config=component_settings)
        elif component_type == GEMINIComponentType.STORAGE:
            return MinioStorageProvider(config=component_settings)
        else:
            return None
        
    def _get_component_settings(self, component_type: GEMINIComponentType) -> object:

        is_local = self.settings.GEMINI_LOCAL 
        
        if component_type == GEMINIComponentType.LOGGER:
            return self.settings.get_logger_config(is_local)
        elif component_type == GEMINIComponentType.STORAGE:
            return self.settings.get_storage_config(is_local)
        elif component_type == GEMINIComponentType.DB:
            return None
        else:
            return None
            
    
