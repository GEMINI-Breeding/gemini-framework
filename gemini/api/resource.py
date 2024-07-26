from typing import Optional, List, Any, Union
from gemini.api.base import APIBase, ID
from gemini.api.data_format import DataFormat
from gemini.models import ResourceModel, ExperimentModel
from gemini.logger import logger_service
from gemini.object_store import storage_service
from pydantic import Field, AliasChoices

import os
import io
from uuid import UUID

class Resource(APIBase):

    db_model = ResourceModel

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "resource_id"))
    resource_uri: Optional[str] = None
    resource_file_name: Optional[str] = None
    is_external: Optional[bool] = None
    resource_info: Optional[dict] = None
    resource_data_format_id: Optional[int] = None
    resource_experiment_id: Optional[Union[str, UUID]] = None


    @classmethod
    def create(
        cls,
        resource_file_path: Any,
        resource_name: str = None,
        resource_tags: dict = None,
        resource_info: dict = {},
        experiment_name: str = 'Default'
    ):
        
        return cls.upload(
            resource_file_path=resource_file_path,
            resource_name=resource_name,
            resource_tags=resource_tags,
            resource_info=resource_info,
            experiment_name=experiment_name,
        )
    
    @classmethod
    def get_by_uri(cls, resource_uri: str) -> "Resource":
        resource = cls.db_model.get_by_parameters(resource_uri=resource_uri)
        resource = cls.model_validate(resource)
        logger_service.info(
            "API", f"Retrieved resource with URI {resource_uri} from the database"
        )
        return resource
    
    @classmethod
    def get_by_experiment(cls, experiment_name: str) -> List["Resource"]:
        experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        resources = experiment.resources
        resources = [cls.model_validate(resource) for resource in resources]
        logger_service.info(
            "API",
            f"Retrieved {len(resources)} resources belonging to {experiment_name} from the database",
        )
        return resources
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved information about {self.resource_name} from the database",
        )
        return self.resource_info
    
    def set_info(self, resource_info: Optional[dict] = None) -> "Resource":
        self.update(resource_info=resource_info)
        logger_service.info(
            "API",
            f"Updated information about {self.resource_name} in the database",
        )
        return self
    
    def add_info(self, resource_info: Optional[dict] = None) -> "Resource":
        current_info = self.get_info()
        updated_info = {**current_info, **resource_info}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Added information to {self.resource_name} in the database",
        )
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Resource":
        current_info = self.get_info()
        updated_info = {k: v for k, v in current_info.items() if k not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Removed information from {self.resource_name} in the database",
        )
        return self
    
    def get_meta_info(self) -> dict:
        self.refresh()
        if self.is_external:
            logger_service.info(
                "API",
                f"Retrieved meta information for {self.resource_name} from the external source",
            )
            return {}
        object_stats = storage_service.stat_file(key=self.resource_uri)
        logger_service.info(
            "API",
            f"Retrieved meta information for {self.resource_name} from the object store",
        )
        return object_stats
    
    @classmethod
    def upload(
        cls,
        resource_file_path: Union[str, bytes, io.BytesIO],
        resource_name: str = None,
        resource_tags: dict = None,
        resource_info: dict = None,
        experiment_name: str = None,
    ):
        
        resource_file_io = None
        resource_data_format = None
        
        if isinstance(resource_file_path, io.BytesIO):
            resource_file_io = resource_file_path
            resource_data_format = (
                DataFormat.get_format_from_file_path(resource_name)
                if resource_name
                else None
            )
        elif isinstance(resource_file_path, str) and os.path.isfile(resource_file_path):
            resource_file_io = open(resource_file_path, "rb")
            resource_name = (
                os.path.basename(resource_file_path)
                if resource_name is None
                else resource_name
            )
            resource_data_format = DataFormat.get_format_from_file_path(resource_file_path)
        
        resource_uri = f"/resources/{experiment_name}/{resource_name}"
        experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        
        resource = ResourceModel.get_or_create(resource_uri=resource_uri)
        resource.resource_name = resource_name
        resource.resource_file_name = resource_name
        resource.resource_data_format_id = resource_data_format.value
        resource.resource_info = resource_info
        resource.resource_uri = resource_uri
        resource.resource_experiment_id = experiment.id if experiment else None
        resource.save()
        
        storage_service.upload_file(
            file_path=resource_file_path if isinstance(resource_file_path, str) else None,
            file_io=resource_file_io if isinstance(resource_file_path, io.BytesIO) else None,
            key=resource_uri,
            tags=resource_tags,
        )
        
        resource = cls.model_validate(resource)
        logger_service.info("API", f"Uploaded {resource_name} to the object store")
        return resource
    
    def download(self, download_path: str) -> str:
        if self.is_external:
            logger_service.info(
                "API",
                f"Downloading {self.resource_name} from the external source",
            )
            return ""
        file_path = storage_service.download_file(
            key=self.resource_uri, file_path=download_path
        )
        logger_service.info(
            "API",
            f"Downloaded {self.resource_name} to {file_path}",
        )
        return file_path
    