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

    def __str__(self):
        return f"SensorType(name={self.sensor_type_name}, id={self.id})"

    def __repr__(self):
        return f"SensorType(sensor_type_name={self.sensor_type_name}, id={self.id})"

    @classmethod
    def exists(
        cls,
        sensor_type_name: str
    ) -> bool:
        try:
            exists = SensorTypeModel.exists(sensor_type_name=sensor_type_name)
            return exists
        except Exception as e:
            print(f"Error checking existence of sensor type: {e}")
            return False

    @classmethod
    def create(
        cls,
        sensor_type_name: str,
        sensor_type_info: dict = {},
    ) -> Optional["SensorType"]:
        try:
            db_instance = SensorTypeModel.get_or_create(
                sensor_type_name=sensor_type_name,
                sensor_type_info=sensor_type_info,
            )
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error creating sensor type: {e}")
            return None

    @classmethod
    def get(cls, sensor_type_name: str) -> Optional["SensorType"]:
        try:
            db_instance = SensorTypeModel.get_by_parameters(sensor_type_name=sensor_type_name)
            if not db_instance:
                print(f"Sensor type with name {sensor_type_name} not found.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting sensor type: {e}")
            return None

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["SensorType"]:
        try:
            db_instance = SensorTypeModel.get(id)
            if not db_instance:
                print(f"Sensor type with ID {id} does not exist.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting sensor type by ID: {e}")
            return None

    @classmethod
    def get_all(cls) -> Optional[List["SensorType"]]:
        try:
            instances = SensorTypeModel.all()
            if not instances or len(instances) == 0:
                print("No sensor types found.")
                return None
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            print(f"Error getting all sensor types: {e}")
            return None

    @classmethod
    def search(
        cls,
        sensor_type_name: str = None,
        sensor_type_info: dict = None
    ) -> Optional[List["SensorType"]]:
        try:
            if not any([sensor_type_name, sensor_type_info]):
                print("At least one search parameter must be provided.")
                return None

            instances = SensorTypeModel.search(
                sensor_type_name=sensor_type_name,
                sensor_type_info=sensor_type_info
            )
            if not instances or len(instances) == 0:
                print("No sensor types found with the provided search parameters.")
                return None
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            print(f"Error searching sensor types: {e}")
            return None

    def update(
        self,
        sensor_type_name: str = None,
        sensor_type_info: dict = None,
    ) -> Optional["SensorType"]:
        try:
            if not any([sensor_type_name, sensor_type_info]):
                print("At least one parameter must be provided for update.")
                return None

            current_id = self.id
            sensor_type = SensorTypeModel.get(current_id)
            if not sensor_type:
                print(f"Sensor type with ID {current_id} does not exist.")
                return None

            sensor_type = SensorTypeModel.update(
                sensor_type,
                sensor_type_name=sensor_type_name,
                sensor_type_info=sensor_type_info
            )
            instance = self.model_validate(sensor_type)
            self.refresh()
            return instance
        except Exception as e:
            print(f"Error updating sensor type: {e}")
            return None

    def delete(self) -> bool:
        try:
            current_id = self.id
            sensor_type = SensorTypeModel.get(current_id)
            if not sensor_type:
                print(f"Sensor type with ID {current_id} does not exist.")
                return False
            SensorTypeModel.delete(sensor_type)
            return True
        except Exception as e:
            print(f"Error deleting sensor type: {e}")
            return False

    def refresh(self) -> Optional["SensorType"]:
        try:
            db_instance = SensorTypeModel.get(self.id)
            if not db_instance:
                print(f"Sensor type with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing sensor type: {e}")
            return None

    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            sensor_type = SensorTypeModel.get(current_id)
            if not sensor_type:
                print(f"Sensor type with ID {current_id} does not exist.")
                return None
            sensor_type_info = sensor_type.sensor_type_info
            if not sensor_type_info:
                print("SensorType info is empty.")
                return None
            return sensor_type_info
        except Exception as e:
            print(f"Error getting sensor type info: {e}")
            return None

    def set_info(self, sensor_type_info: dict) -> Optional["SensorType"]:
        try:
            current_id = self.id
            sensor_type = SensorTypeModel.get(current_id)
            if not sensor_type:
                print(f"Sensor type with ID {current_id} does not exist.")
                return None
            sensor_type = SensorTypeModel.update(
                sensor_type,
                sensor_type_info=sensor_type_info,
            )
            instance = self.model_validate(sensor_type)
            self.refresh()
            return instance
        except Exception as e:
            print(f"Error setting sensor type info: {e}")
            return None
