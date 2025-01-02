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
            instances = DataFormatModel.get_all()
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            raise e
        
    @classmethod
    def search(cls, **search_parameters) -> List["DataFormat"]:
        try:
            data_formats = DataFormatModel.search(**search_parameters)
            data_formats = [cls.model_validate(data_format) for data_format in data_formats]
            return data_formats
        except Exception as e:
            raise e
    
    def update(self, **update_parameters) -> "DataFormat":
        return super().update(**update_parameters)
    
    def delete(self) -> bool:
        try:
            current_id = self.id
            data_format = DataFormatModel.get(current_id)
            data_format.delete()
            return True
        except Exception as e:
            raise e
        
    
    def refresh(self) -> "DataFormat":
        return super().refresh()
