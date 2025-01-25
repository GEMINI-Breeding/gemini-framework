import os
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import model_validator
from typing import Any, Optional, Union, ClassVar
from uuid import UUID


from abc import ABC, abstractmethod

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

    @abstractmethod
    def _preprocess_record(cls, record: dict) -> dict:
        pass

    @abstractmethod
    def _postprocess_record(cls, record: dict) -> dict:
        pass

    @abstractmethod
    def _upload_file(cls, file_key: str, absolute_file_path: str) -> str:
        pass

    @abstractmethod
    def _download_file(cls, file_url: str, save_path: str) -> str:
        pass

    @abstractmethod
    def _get_file_download_url(cls, file_key: str) -> str:
        pass

    @abstractmethod
    def _get_file_uri(cls, absolute_file_path: str, record: dict) -> str:
        pass

        
