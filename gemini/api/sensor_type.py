from typing import Optional, List
from gemini.api.base import APIBase, ID
from gemini.server.database.models import SensorTypeModel

from pydantic import Field, AliasChoices


class SensorType(APIBase):

    db_model = SensorTypeModel

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "sensor_type_id"))
    sensor_type_name: str
    sensor_type_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        sensor_type_name: str,
        sensor_type_info: dict = None,
    ):
        """
        Create a new sensor type

        Args:
        sensor_type_name (str): The name of the sensor type
        sensor_type_info (dict, optional): The information about the sensor type. Defaults to None.

        Returns:
        SensorType: The created sensor type
        """
        new_instance = cls.db_model.get_or_create(
            sensor_type_name=sensor_type_name,
            sensor_type_info=sensor_type_info,
        )
        new_instance = cls.model_validate(new_instance)
        return new_instance
    
    @classmethod
    def get_by_id(cls, sensor_type_id: int) -> "SensorType":
        """
        Get a sensor type by its ID

        Args:
        sensor_type_id (int): The ID of the sensor type

        Returns:
        SensorType: The sensor type with the given ID
        """
        sensor_type = cls.db_model.get_by_id(sensor_type_id)
        sensor_type = cls.model_validate(sensor_type)
        return sensor_type
    
    def get_info(self) -> dict:
        """
        Get the information about a sensor type

        Returns:
        dict: The information about the sensor type
        """
        self.refresh()
        return self.sensor_type_info
    
    def set_info(self, sensor_type_info: Optional[dict] = None) -> "SensorType":
        """
        Set the information about a sensor type

        Args:
        sensor_type_info (Optional[dict], optional): The information to set. Defaults to None.

        Returns:
        SensorType: The sensor type with the updated information
        """
        self.update(sensor_type_info=sensor_type_info)
        return self
    
    def add_info(self, sensor_type_info: Optional[dict] = None) -> "SensorType":
        """
        Add information to a sensor type

        Args:
        sensor_type_info (Optional[dict], optional): The information to add. Defaults to None.

        Returns:
        SensorType: The sensor type with the added information
        """
        current_info = self.get_info()
        updated_info = {**current_info, **sensor_type_info}
        self.set_info(updated_info)
        return self
    
    @classmethod
    def remove_info(cls, keys_to_remove: List[str]) -> "SensorType":
        """
        Remove information from a sensor type

        Args:
        keys_to_remove (List[str]): The keys to remove from the sensor type information

        Returns:
        SensorType: The sensor type with the removed information
        """
        current_info = cls.get_info()
        updated_info = {
            key: value
            for key, value in current_info.items()
            if key not in keys_to_remove
        }
        cls.set_info(updated_info)
        return cls


