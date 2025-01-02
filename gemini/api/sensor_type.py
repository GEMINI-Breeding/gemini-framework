from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.db.models.sensor_types import SensorTypeModel

class SensorType(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "sensor_type_id"))

    sensor_type_name: str
    sensor_type_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        sensor_type_name: str,
        sensor_type_info: dict = {},
    ) -> "SensorType":
        try:
            instance = SensorTypeModel.get_or_create(
                sensor_type_name=sensor_type_name,
                sensor_type_info=sensor_type_info,
            )
            instance = cls.model_validate(instance)
            return instance
        except Exception as e:
            raise e
        
    @classmethod
    def get(cls, sensor_type_name: str) -> "SensorType":
        try:
            instance = SensorTypeModel.get_by_parameters(sensor_type_name=sensor_type_name)
            instance = cls.model_validate(instance)
            return instance
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "SensorType":
        try:
            instance = SensorTypeModel.get(id)
            instance = cls.model_validate(instance)
            return instance
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["SensorType"]:
        try:
            instances = SensorTypeModel.get_all()
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            raise e
        

    @classmethod
    def search(
        cls,
        sensor_type_name: str = None,
        sensor_type_info: dict = None,
    ) -> List["SensorType"]:
        try:
            instances = SensorTypeModel.search(
                sensor_type_name=sensor_type_name,
                sensor_type_info=sensor_type_info,
            )
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            raise e
        

    def update(self, **update_parameters) -> "SensorType":
        return super().update(**update_parameters)
    
    def delete(self) -> bool:
        return super().delete()
    
    def refresh(self) -> "SensorType":
        return super().refresh()
    

        

