import os
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import computed_field
from pydantic import model_validator
from typing import Any, Optional, Union, ClassVar
from uuid import UUID

from gemini.storage.providers.minio_storage import MinioStorageProvider
from gemini.config.settings import GEMINISettings
from gemini.manager import GEMINIManager, GEMINIComponentType

from functools import cached_property
from abc import ABC, abstractmethod

manager = GEMINIManager()

class APIBase(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        protected_namespaces=(),
        extra="allow"
    )

    @classmethod
    @abstractmethod
    def create(cls, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def get_by_id(cls, id: Union[UUID, int, str]):
        pass

    @classmethod
    @abstractmethod
    def get_all(cls):
        pass

    @classmethod
    @abstractmethod
    def get(cls, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def search(cls, **search_parameters):
        pass

    @abstractmethod
    def update(self, **kwargs):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def refresh(self):
        pass

class FileHandlerMixin(BaseModel):

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    minio_storage_provider: ClassVar[MinioStorageProvider] = manager.get_component_provider(GEMINIComponentType.STORAGE)

    @classmethod
    @abstractmethod
    def _preprocess_record(cls, record: 'APIBase') -> 'APIBase':
        pass

    @classmethod
    @abstractmethod
    def _postprocess_record(cls, record: dict) -> dict:
        pass

    @classmethod
    @abstractmethod
    def _upload_file(cls, file_key: str, absolute_file_path: str) -> str:
        pass

    @abstractmethod
    def _download_file(self, output_folder: str) -> str:
        pass

    @abstractmethod
    def _get_file_download_url(self, record_file_key: str) -> str:
        pass

    @classmethod
    @abstractmethod
    def _create_file_uri(cls, record: 'APIBase') -> str:
        pass

        
