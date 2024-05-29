from typing import Optional, List, Any
from gemini.api.base import APIBase
from gemini.api.enums import GEMINIDatasetType
from gemini.api.dataset_type import DatasetType
from gemini.models import DatasetModel, ExperimentModel, DatasetTypeModel
from gemini.logger import logger_service

from datetime import datetime, date


class Dataset(APIBase):

    db_model = DatasetModel

    dataset_name: str
    dataset_info: Optional[dict] = None
    is_derived: Optional[bool] = False
    collection_date: Optional[date] = None

    dataset_type: Optional[DatasetType] = None

    @classmethod
    def create(
        cls,
        dataset_name: str,
        dataset_info: dict = None,
        is_derived: bool = False,
        collection_date: date = None,
        dataset_type: GEMINIDatasetType = GEMINIDatasetType.Default
    ):
        
        db_dataset_type = DatasetTypeModel.get_by_id(dataset_type.value)
        new_instance = cls.db_model.get_or_create(
            dataset_name=dataset_name,
            dataset_info=dataset_info,
            is_derived=is_derived,
            collection_date=collection_date,
            dataset_type=db_dataset_type
        )
        logger_service.info(
            "API",
            f"Created a new dataset with name {new_instance.dataset_name} in the database",
        )
        new_instance = cls.model_validate(new_instance)
        return new_instance
    
    @classmethod
    def get(cls, dataset_name: str) -> "Dataset":
        db_instance = cls.db_model.get_by_parameters(dataset_name=dataset_name)
        logger_service.info("API", f"Retrieved dataset with name {dataset_name} from the database")
        return cls.model_validate(db_instance)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.dataset_name} from the database")
        return self.dataset_info
    
    def set_info(self, dataset_info: Optional[dict] = None) -> "Dataset":
        self.update(dataset_info=dataset_info)
        logger_service.info("API", f"Set information about {self.dataset_name} in the database")
        return self
    
    def add_info(self, dataset_info: dict) -> "Dataset":
        current_info = self.get_info()
        updated_info = {**current_info, **dataset_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information about {self.dataset_name} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Dataset":
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(current_info)
        logger_service.info("API", f"Removed information from {self.dataset_name} in the database")
        return self
    
    # Todo: Add Records and Search Records methods

