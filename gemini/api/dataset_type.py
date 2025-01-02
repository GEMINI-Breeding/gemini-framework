from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.data_format import DataFormat

from gemini.db.models.dataset_types import DatasetTypeModel

class DatasetType(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "dataset_type_id"))

    dataset_type_name: str
    dataset_type_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        dataset_type_name: str,
        dataset_type_info: dict = {},
    ) -> "DatasetType":
        try:
            instance = DatasetTypeModel.get_or_create(
                dataset_type_name=dataset_type_name,
                dataset_type_info=dataset_type_info,
            )
            instance = cls.model_validate(instance)
            return instance
        except Exception as e:
            raise e
        

    @classmethod
    def get(cls, dataset_type_name: str) -> "DatasetType":
        try:
            instance = DatasetTypeModel.get_by_parameters(dataset_type_name=dataset_type_name)
            instance = cls.model_validate(instance)
            return instance
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "DatasetType":
        try:
            instance = DatasetTypeModel.get(id)
            instance = cls.model_validate(instance)
            return instance
        except Exception as e:
            raise e
        
    @classmethod
    def get_all(cls) -> List["DatasetType"]:
        try:
            instances = DatasetTypeModel.get_all()
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            raise e
        
    @classmethod
    def search(cls, **search_parameters):
        try:
            instances = DatasetTypeModel.search(**search_parameters)
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            raise e
        
    def update(self, **update_parameters) -> "DatasetType":
        return super().update(**update_parameters)
    
    def delete(self) -> bool:
        return super().delete()
        
    def refresh(self):
        return super().refresh()