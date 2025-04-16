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
    def exists(
        cls,
        sensor_type_name: str
    ) -> bool:
        try:
            exists = SensorTypeModel.exists(sensor_type_name=sensor_type_name)
            return exists
        except Exception as e:
            raise e

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
            instance = cls.model_validate(instance) if instance else None
            return instance
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "SensorType":
        try:
            instance = SensorTypeModel.get(id)
            instance = cls.model_validate(instance)
            return instance if instance else None
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["SensorType"]:
        try:
            instances = SensorTypeModel.all()
            instances = [cls.model_validate(instance) for instance in instances]
            return instances if instances else None
        except Exception as e:
            raise e
        

    @classmethod
    def search(
        cls,
        sensor_type_name: str = None,
        sensor_type_info: dict = None,
    ) -> List["SensorType"]:
        try:
            if not sensor_type_name and not sensor_type_info:
                raise Exception("Must provide at least one search parameter.")

            instances = SensorTypeModel.search(
                sensor_type_name=sensor_type_name,
                sensor_type_info=sensor_type_info,
            )
            instances = [cls.model_validate(instance) for instance in instances]
            return instances if instances else None
        except Exception as e:
            raise e
        

    def update(
            self, 
            sensor_type_name: str = None,
            sensor_type_info: dict = None
        ) -> "SensorType":
        try:
            if not sensor_type_name and not sensor_type_info:
                raise ValueError("At least one parameter must be provided.")
            
            current_id = self.id
            sensor_type = SensorTypeModel.get(current_id)
            sensor_type = SensorTypeModel.update(
                sensor_type,
                sensor_type_name=sensor_type_name,
                sensor_type_info=sensor_type_info,
            )
            sensor_type = self.model_validate(sensor_type)
            self.refresh()
            return sensor_type
        except Exception as e:
            raise e
    
    def delete(self) -> bool:
        try:
            current_id = self.id
            sensor_type = SensorTypeModel.get(current_id)
            SensorTypeModel.delete(sensor_type)
            return True
        except Exception as e:
            raise e
        
    def get_info(self) -> dict:
        try:
            current_id = self.id
            sensor_type = SensorTypeModel.get(current_id)
            sensor_type_info = sensor_type.sensor_type_info
            if not sensor_type_info:
                raise Exception("SensorType info is empty.")
            return sensor_type_info
        except Exception as e:
            raise e
        
    def set_info(self, sensor_type_info: dict) -> "SensorType":
        try:
            current_id = self.id
            sensor_type = SensorTypeModel.get(current_id)
            sensor_type = SensorTypeModel.update(
                sensor_type,
                sensor_type_info=sensor_type_info
            )
            sensor_type = self.model_validate(sensor_type)
            self.refresh()
            return self
        except Exception as e:
            raise e

        
    def refresh(self) -> "SensorType":
        try:
            db_instance = SensorTypeModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e
