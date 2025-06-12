from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.enums import GEMINIDatasetType
from gemini.db.models.dataset_types import DatasetTypeModel

class DatasetType(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "dataset_type_id"))

    dataset_type_name: str
    dataset_type_info: Optional[dict] = None

    def __str__(self):
        return f"DatasetType(name={self.dataset_type_name}, id={self.id})"

    def __repr__(self):
        return f"DatasetType(dataset_type_name={self.dataset_type_name}, id={self.id})"

    @classmethod
    def exists(
        cls,
        dataset_type_name: str
    ) -> bool:
        try:
            exists = DatasetTypeModel.exists(dataset_type_name=dataset_type_name)
            return exists
        except Exception as e:
            print(f"Error checking existence of dataset type: {e}")
            return False

    @classmethod
    def create(
        cls,
        dataset_type_name: str,
        dataset_type_info: dict = {},
    ) -> Optional["DatasetType"]:
        try:
            db_instance = DatasetTypeModel.get_or_create(
                dataset_type_name=dataset_type_name,
                dataset_type_info=dataset_type_info,
            )
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error creating dataset type: {e}")
            return None

    @classmethod
    def get(cls, dataset_type_name: str) -> Optional["DatasetType"]:
        try:
            db_instance = DatasetTypeModel.get_by_parameters(dataset_type_name=dataset_type_name)
            if not db_instance:
                print(f"Dataset type with name {dataset_type_name} not found.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting dataset type: {e}")
            return None

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["DatasetType"]:
        try:
            db_instance = DatasetTypeModel.get(id)
            if not db_instance:
                print(f"Dataset type with ID {id} does not exist.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting dataset type by ID: {e}")
            return None

    @classmethod
    def get_all(cls) -> Optional[List["DatasetType"]]:
        try:
            instances = DatasetTypeModel.all()
            if not instances or len(instances) == 0:
                print("No dataset types found.")
                return None
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            print(f"Error getting all dataset types: {e}")
            return None

    @classmethod
    def search(
        cls,
        dataset_type_name: str = None,
        dataset_type_info: dict = None
    ) -> Optional[List["DatasetType"]]:
        try:
            if not any([dataset_type_name, dataset_type_info]):
                print("At least one search parameter must be provided.")
                return None

            instances = DatasetTypeModel.search(
                dataset_type_name=dataset_type_name,
                dataset_type_info=dataset_type_info
            )
            if not instances or len(instances) == 0:
                print("No dataset types found with the provided search parameters.")
                return None
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            print(f"Error searching dataset types: {e}")
            return None

    def update(
            self,
            dataset_type_name: str = None,
            dataset_type_info: dict = None
        ) -> Optional["DatasetType"]:
        try:
            if not any([dataset_type_name, dataset_type_info]):
                print("At least one parameter must be provided for update.")
                return None

            current_id = self.id
            dataset_type = DatasetTypeModel.get(current_id)
            if not dataset_type:
                 print(f"Dataset type with ID {current_id} does not exist.")
                 return None

            dataset_type = DatasetTypeModel.update(
                dataset_type,
                dataset_type_name=dataset_type_name,
                dataset_type_info=dataset_type_info,
            )
            instance = self.model_validate(dataset_type)
            self.refresh()
            return instance
        except Exception as e:
            print(f"Error updating dataset type: {e}")
            return None

    def delete(self) -> bool:
        try:
            current_id = self.id
            dataset_type = DatasetTypeModel.get(current_id)
            if not dataset_type:
                 print(f"Dataset type with ID {current_id} does not exist.")
                 return False
            DatasetTypeModel.delete(dataset_type)
            return True
        except Exception as e:
            print(f"Error deleting dataset type: {e}")
            return False

    def refresh(self) -> Optional["DatasetType"]:
        try:
            db_instance = DatasetTypeModel.get(self.id)
            if not db_instance:
                print(f"Dataset type with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing dataset type: {e}")
            return None

    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            dataset_type = DatasetTypeModel.get(current_id)
            if not dataset_type:
                print(f"Dataset type with ID {current_id} does not exist.")
                return None
            dataset_type_info = dataset_type.dataset_type_info
            if not dataset_type_info:
                print("DatasetType info is empty.")
                return None
            return dataset_type_info
        except Exception as e:
            print(f"Error getting dataset type info: {e}")
            return None

    def set_info(self, dataset_type_info: dict) -> Optional["DatasetType"]:
        try:
            current_id = self.id
            dataset_type = DatasetTypeModel.get(current_id)
            if not dataset_type:
                print(f"Dataset type with ID {current_id} does not exist.")
                return None
            dataset_type = DatasetTypeModel.update(
                dataset_type,
                dataset_type_info=dataset_type_info,
            )
            instance = self.model_validate(dataset_type)
            self.refresh()
            return instance
        except Exception as e:
            print(f"Error setting dataset type info: {e}")
            return None