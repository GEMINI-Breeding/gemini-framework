from typing import Any, Optional, List
from gemini.api.base import APIBase
from gemini.models import DatasetTypeModel
from gemini.logger import logger_service


class DatasetType(APIBase):

    db_model = DatasetTypeModel

    dataset_type_name: str
    dataset_type_info: Optional[dict] = None


    @classmethod
    def create(cls, dataset_type_name: str, dataset_type_info: dict = None):
        db_instance = cls.db_model.get_or_create(
            dataset_type_name=dataset_type_name,
            dataset_type_info=dataset_type_info,
        )
        logger_service.info("API", f"Created a new dataset type with name {db_instance.dataset_type_name} in the database")
        return cls.model_validate(db_instance)
    
    @classmethod
    def get(cls, dataset_type_name: str) -> "DatasetType":
        db_instance = cls.db_model.get_by_parameters(dataset_type_name=dataset_type_name)
        logger_service.info("API", f"Retrieved dataset type with name {dataset_type_name} from the database")
        return cls.model_validate(db_instance)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.dataset_type_name} from the database")
        return self.dataset_type_info
    
    def set_info(self, dataset_type_info: Optional[dict] = None) -> "DatasetType":
        self.update(dataset_type_info=dataset_type_info)
        logger_service.info("API", f"Set information about {self.dataset_type_name} in the database")
        return self 

    def add_info(self, dataset_type_info: dict) -> "DatasetType":
        current_info = self.get_info()
        updated_info = {**current_info, **dataset_type_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information about {self.dataset_type_name} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "DatasetType":
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info("API", f"Removed information from {self.dataset_type_name} in the database")
        return self
