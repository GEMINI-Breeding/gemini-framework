from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.data_format import DataFormat
from gemini.db.models.data_types import DataTypeModel
from gemini.db.models.associations import DataTypeFormatModel

class DataType(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "data_type_id"))

    data_type_name: str
    data_type_info: Optional[dict] = None

    formats: List[DataFormat] = None
    
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
            instances = DataTypeModel.all()
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            raise e
        

    @classmethod
    def search(
        cls, 
        data_type_name: str = None,
        data_type_info: dict = None
    ) -> List["DataType"]:
        try:
            if not data_type_name and not data_type_info:
                raise ValueError("At least one parameter must be provided.")
            
            instances = DataTypeModel.search(
                data_type_name=data_type_name,
                data_type_info=data_type_info
            )
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            raise e
        

    def update(
        self,
        data_type_info: dict = None,
    ) -> "DataType":
        try:
            if not data_type_info:
                raise ValueError("At least one parameter must be provided.")

            current_id = self.id
            data_type = DataTypeModel.get(current_id)
            data_type.update(data_type, data_type_info=data_type_info)
            data_type = self.model_validate(data_type)
            data_type.refresh()
            return data_type
        except Exception as e:
            raise e
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            data_type = DataTypeModel.get(current_id)
            DataTypeModel.delete(data_type)
            return True
        except Exception as e:
            raise e
        
    def refresh(self) -> "DataType":
        try:
            db_instance = DataTypeModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key):
                    actual_value = getattr(instance, key)
                    setattr(self, key, actual_value)
            return self
        except Exception as e:
            raise e
        
    def get_formats(self) -> List["DataFormat"]:
        try:
            data_formats = self.formats
            data_formats = [DataFormat.model_validate(data_format) for data_format in data_formats]
            return data_formats
        except Exception as e:
            raise e
        
    def create_format(
        self,
        data_format_name: str,
        data_format_mime_type: str,
        data_format_info: dict = {}
    ) -> "DataFormat":
        try:
            data_format = DataFormat.create(
                data_format_name=data_format_name,
                data_format_mime_type=data_format_mime_type,
                data_format_info=data_format_info
            )
            DataTypeFormatModel.get_or_create(
                data_type_id=self.id,
                data_format_id=data_format.id
            )
            return data_format
        except Exception as e:
            raise e


