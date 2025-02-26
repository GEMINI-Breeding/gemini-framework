from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.db.models.data_formats import DataFormatModel

class DataFormat(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "data_format_id"))

    data_format_name: str
    data_format_mime_type: Optional[str] = None
    data_format_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        data_format_name: str,
        data_format_mime_type: str = None,
        data_format_info: dict = {},
    ) -> "DataFormat":
        try:
            instance = DataFormatModel.get_or_create(
                data_format_name=data_format_name,
                data_format_mime_type=data_format_mime_type,
                data_format_info=data_format_info,
            )
            instance = cls.model_validate(instance)
            return instance
        except Exception as e:
            raise e
        

    @classmethod
    def get(cls, data_format_name: str) -> "DataFormat":
        try:
            instance = DataFormatModel.get_by_parameters(data_format_name=data_format_name)
            instance = cls.model_validate(instance)
            return instance
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "DataFormat":
        try:
            instance = DataFormatModel.get(id)
            instance = cls.model_validate(instance)
            return instance
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["DataFormat"]:
        try:
            instances = DataFormatModel.all()
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            raise e
        
    @classmethod
    def search(
        cls,
        data_format_name: str = None,
        data_format_mime_type: str = None,
        data_format_info: dict = None 
    ) -> List["DataFormat"]:
        try:

            if not data_format_name and not data_format_mime_type and not data_format_info:
                raise ValueError("At least one parameter must be provided")

            data_formats = DataFormatModel.search(
                data_format_name=data_format_name,
                data_format_mime_type=data_format_mime_type,
                data_format_info=data_format_info,
            )
            data_formats = [cls.model_validate(data_format) for data_format in data_formats]
            return data_formats
        except Exception as e:
            raise e
    
    def update(
        self,
        data_format_mime_type: str = None,
        data_format_info: dict = None,       
    ) -> "DataFormat":
        try:

            if not data_format_mime_type and not data_format_info:
                raise ValueError("At least one parameter must be provided")

            current_id = self.id
            data_format = DataFormatModel.get(current_id)
            data_format = DataFormatModel.update(
                data_format,
                data_format_mime_type=data_format_mime_type,
                data_format_info=data_format_info,
            )
            data_format = self.model_validate(data_format)
            self.refresh()
            return data_format
        except Exception as e:
            raise e
    
    def delete(self) -> bool:
        try:
            current_id = self.id
            data_format = DataFormatModel.get(current_id)
            DataFormatModel.delete(data_format)
            return True
        except Exception as e:
            raise e
        
    
    def refresh(self) -> "DataFormat":
        try:
            db_instance = DataFormatModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e
