from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.data_format import DataFormat
from gemini.db.models.data_types import DataTypeModel

class DataType(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "data_type_id"))

    data_type_name: str
    data_type_info: Optional[dict] = None

    formats: List[DataFormat]
    
    @classmethod
    def create(
        cls,
        data_type_name: str,
        data_type_info: dict = {},
    ) -> "DataType":
        try:
            instance = DataTypeModel.get_or_create(
                data_type_name=data_type_name,
                data_type_info=data_type_info,
            )
            instance = cls.model_validate(instance)
            return instance
        except Exception as e:
            raise e
        
    @classmethod
    def get(cls, data_type_name: str) -> "DataType":
        try:
            instance = DataTypeModel.get_by_parameters(data_type_name=data_type_name)
            instance = cls.model_validate(instance)
            return instance
        except Exception as e:
            raise e
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "DataType":
        try:
            instance = DataTypeModel.get(id)
            instance = cls.model_validate(instance)
            return instance
        except Exception as e:
            raise e
        
    @classmethod
    def get_all(cls) -> List["DataType"]:
        try:
            instances = DataTypeModel.get_all()
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            raise e
        

    @classmethod
    def search(cls, **search_parameters) -> List["DataType"]:
        try:
            instances = DataTypeModel.search(**search_parameters)
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            raise e
        
    def update(self, **update_parameters) -> "DataType":
        return super().update(**update_parameters)
    
    def delete(self) -> bool:
        return super().delete()
        
    def refresh(self):
        return super().refresh()

    def get_formats(self) -> List["DataFormat"]:
        try:
            data_formats = self.formats
            return data_formats
        except Exception as e:
            raise e


