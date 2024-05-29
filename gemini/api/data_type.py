from typing import Any, Optional, List
from gemini.api.base import APIBase
from gemini.api.data_format import DataFormat
from gemini.models import DataTypeModel, DataFormatModel
from gemini.logger import logger_service


class DataType(APIBase):

    db_model = DataTypeModel

    data_type_name: str
    data_type_info: Optional[dict] = None

    formats: Optional[List[DataFormat]] = None

    @classmethod
    def create(cls, data_type_name: str, data_type_info: dict = None):
        db_instance = cls.db_model.get_or_create(
            data_type_name=data_type_name,
            data_type_info=data_type_info,
        )
        logger_service.info(
            "API",
            f"Created a new data type with name {db_instance.data_type_name} in the database",
        )
        return cls.model_validate(db_instance)
    
    @classmethod
    def get(cls, data_type_name: str) -> "DataType":
        db_instance = cls.db_model.get_by_parameters(data_type_name=data_type_name)
        logger_service.info(
            "API",
            f"Retrieved data type with name {db_instance.data_type_name} from the database",
        )
        return cls.model_validate(db_instance)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved information about {self.data_type_name} from the database",
        )
        return self.data_type_info
    
    def set_info(self, data_type_info: Optional[dict] = None) -> "DataType":
        self.update(data_type_info=data_type_info)
        logger_service.info(
            "API",
            f"Set information about {self.data_type_name} in the database",
        )
        return self
    
    def add_info(self, data_type_info: Optional[dict] = None) -> "DataType":
        current_info = self.get_info()
        updated_info = {**current_info, **data_type_info}
        self.set_info(updated_info)
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "DataType":
        current_info = self.get_info()
        updated_info = {
            key: value
            for key, value in current_info.items()
            if key not in keys_to_remove
        }
        self.set_info(updated_info)
        return self
    
    @classmethod
    def get_data_formats(cls, data_type_name: str) -> List[DataFormat]:
        data_type = cls.get(data_type_name)
        data_formats = data_type.formats
        logger_service.info(
            "API",
            f"Retrieved formats for {data_type.data_type_name} from the database",
        )
        return data_formats


