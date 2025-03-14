from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
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
            instance = cls.model_validate(instance) if instance else None
            return instance
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "DatasetType":
        try:
            instance = DatasetTypeModel.get(id)
            instance = cls.model_validate(instance) if instance else None
            return instance
        except Exception as e:
            raise e
        
    @classmethod
    def get_all(cls) -> List["DatasetType"]:
        try:
            instances = DatasetTypeModel.all()
            instances = [cls.model_validate(instance) for instance in instances]
            return instances if instances else None
        except Exception as e:
            raise e
        
    @classmethod
    def search(
        cls,
        dataset_type_name: str = None,
        dataset_type_info: dict = None
    ):
        try:
            if not dataset_type_name and not dataset_type_info:
                raise ValueError("At least one search parameter must be provided.")

            instances = DatasetTypeModel.search(
                dataset_type_name=dataset_type_name,
                dataset_type_info=dataset_type_info
            )
            instances = [cls.model_validate(instance) for instance in instances]
            return instances if instances else None
        except Exception as e:
            raise e
        
    def update(
            self,
            dataset_type_name: str = None, 
            dataset_type_info: dict = None
        ) -> "DatasetType":
        try:
            if not dataset_type_info and not dataset_type_name:
                raise ValueError("At least one parameter must be provided.")
            
            current_id = self.id
            dataset_type = DatasetTypeModel.get(current_id)
            dataset_type = DatasetTypeModel.update(
                dataset_type,
                dataset_type_name=dataset_type_name,
                dataset_type_info=dataset_type_info,
            )
            dataset_type = self.model_validate(dataset_type)
            self.refresh()
            return dataset_type
        except Exception as e:
            raise e
    
    def delete(self) -> bool:
        try:
            current_id = self.id
            dataset_type = DatasetTypeModel.get(current_id)
            DatasetTypeModel.delete(dataset_type)
            return True
        except Exception as e:
            raise e

        
    def refresh(self) -> "DatasetType":
        try:
            db_instance = DatasetTypeModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e