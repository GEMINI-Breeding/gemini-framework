from typing import Any, Optional, List
from gemini.api.base import APIBase
from gemini.models import DataFormatModel, DataTypeModel
from gemini.logger import logger_service


class DataFormat(APIBase):

    db_model = DataFormatModel

    data_format_name: str
    data_format_mime_type: Optional[str] = None
    data_format_info: Optional[dict] = None


    @classmethod
    def create(
        cls,
        data_format_name: str,
        data_format_mime_type: str = None,
        data_format_info: dict = None,
    ):
        db_instance = cls.db_model.get_or_create(
            data_format_name=data_format_name,
            data_format_mime_type=data_format_mime_type,
            data_format_info=data_format_info,
        )

        logger_service.info(
            "API",
            f"Created a new data format with name {db_instance.data_format_name} in the database",
        )

        return cls.model_validate(db_instance)

    @classmethod
    def get(cls, data_format_name: str) -> "DataFormat":
        db_instance = cls.db_model.get_by_parameters(data_format_name=data_format_name)
        logger_service.info("API", f"Retrieved data format with name {data_format_name} from the database")
        return cls.model_validate(db_instance)
    
    @classmethod
    def get_format_from_file_path(cls, file_path: str):
        file_extension = file_path.split(".")[-1]
        data_formats = cls.db_model.search(data_format_name=file_extension)
        data_formats = [cls.model_validate(data_format) for data_format in data_formats]
        logger_service.info("API", f"Retrieved data format from file path {file_path}")
        return data_formats
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.data_format_name} from the database")
        return self.data_format_info
    
    def set_info(self, data_format_info: Optional[dict] = None) -> "DataFormat":
        self.update(data_format_info=data_format_info)
        logger_service.info("API", f"Set information about {self.data_format_name} in the database")
        return self
    
    def add_info(self, data_format_info: Optional[dict] = None) -> "DataFormat":
        current_info = self.get_info()
        updated_info = {**current_info, **data_format_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information to {self.data_format_name} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "DataFormat":
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info("API", f"Removed information from {self.data_format_name} in the database")
        return self
    