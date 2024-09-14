from typing import Optional, List, Any
from gemini.api.base import APIBase, ID
from gemini.server.database.models import SensorPlatformModel, SensorModel
from pydantic import Field, AliasChoices


class SensorPlatform(APIBase):
    """
    Represents a sensor platform in the Gemini framework.
    """

    db_model = SensorPlatformModel

    id: Optional[ID] = Field(
        None, validation_alias=AliasChoices("id", "sensor_platform_id")
    )
    sensor_platform_name: str
    sensor_platform_info: Optional[dict] = None

    @classmethod
    def create(
        cls, sensor_platform_name: str = "Default", sensor_platform_info: dict = {}
    ) -> "SensorPlatform":
        """
        Creates a new sensor platform with the given name and information.

        Args:
            sensor_platform_name (str, optional): The name of the sensor platform. Defaults to 'Default'.
            sensor_platform_info (dict, optional): Additional information about the sensor platform. Defaults to {}.

        Returns:
            SensorPlatform: The created sensor platform instance.
        """
        db_instance = cls.db_model.get_or_create(
            sensor_platform_name=sensor_platform_name,
            sensor_platform_info=sensor_platform_info,
        )
        instance = cls.model_validate(db_instance)
        return instance

    @classmethod
    def get(cls, sensor_platform_name: str) -> "SensorPlatform":
        """
        Retrieves a sensor platform by its name.

        Args:
            sensor_platform_name (str): The name of the sensor platform to retrieve.

        Returns:
            SensorPlatform: The retrieved sensor platform instance.
        """
        db_instance = SensorPlatformModel.get_by_parameters(
            sensor_platform_name=sensor_platform_name
        )
        return cls.model_validate(db_instance)

    def get_info(self) -> dict:
        """
        Retrieves the information associated with the sensor platform.

        Returns:
            dict: The information associated with the sensor platform.
        """
        self.refresh()
        return self.sensor_platform_info

    def set_info(self, sensor_platform_info: Optional[dict] = None) -> "SensorPlatform":
        """
        Sets the information associated with the sensor platform.

        Args:
            sensor_platform_info (dict, optional): The new information to set. Defaults to None.

        Returns:
            SensorPlatform: The updated sensor platform instance.
        """
        self.update(sensor_platform_info=sensor_platform_info)
        return self

    def add_info(self, sensor_platform_info: Optional[dict] = None) -> "SensorPlatform":
        """
        Adds additional information to the sensor platform.

        Args:
            sensor_platform_info (dict, optional): The additional information to add. Defaults to None.

        Returns:
            SensorPlatform: The updated sensor platform instance.
        """
        current_info = self.get_info()
        updated_info = {**current_info, **sensor_platform_info}
        self.set_info(updated_info)
        return self

    def remove_info(self, keys_to_remove: List[str]) -> "SensorPlatform":
        """
        Removes specific keys from the information associated with the sensor platform.

        Args:
            keys_to_remove (List[str]): The keys to remove from the information.

        Returns:
            SensorPlatform: The updated sensor platform instance.
        """
        current_info = self.get_info()
        updated_info = {
            k: v for k, v in current_info.items() if k not in keys_to_remove
        }
        self.set_info(updated_info)
        return self

    # Todo: Get all sensors on a sensor platform, add a sensor to a sensor platform, remove a sensor from a sensor platform
    def get_sensors():
        pass

    def add_sensor():
        pass

    def remove_sensor():
        pass
