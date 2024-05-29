from typing import Optional, List, Any
from gemini.api.base import APIBase
from gemini.models import SensorPlatformModel, SensorModel
from gemini.logger import logger_service


class SensorPlatform(APIBase):

    db_model = SensorPlatformModel

    sensor_platform_name: str
    sensor_platform_info: Optional[dict] = None


    @classmethod
    def create(
        cls,
        sensor_platform_name: str,
        sensor_platform_info: dict = None
    ):
        db_instance = cls.db_model.get_or_create(
            sensor_platform_name=sensor_platform_name,
            sensor_platform_info=sensor_platform_info
        )
        instance = cls.model_validate(db_instance)
        logger_service.info(
            "API",
            f"Created a new instance of {cls.__name__} with id {instance.id}",
        )
        return instance
    
    @classmethod
    def get(cls, sensor_platform_name: str) -> "SensorPlatform":
        db_instance = SensorPlatformModel.get_by_parameters(sensor_platform_name=sensor_platform_name)
        logger_service.info("API", f"Retrieved sensor platform with name {sensor_platform_name} from the database")
        return cls.model_validate(db_instance)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.sensor_platform_name} from the database")
        return self.sensor_platform_info
    
    def set_info(self, sensor_platform_info: Optional[dict] = None) -> "SensorPlatform":
        self.update(sensor_platform_info=sensor_platform_info)
        logger_service.info("API", f"Set information about {self.sensor_platform_name} in the database")
        return self
    
    def add_info(self, sensor_platform_info: Optional[dict] = None) -> "SensorPlatform":
        current_info = self.get_info()
        updated_info = {**current_info, **sensor_platform_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information to {self.sensor_platform_name} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "SensorPlatform":
        current_info = self.get_info()
        updated_info = {k: v for k, v in current_info.items() if k not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info("API", f"Removed information from {self.sensor_platform_name} in the database")
        return self
    
    # Todo: Get all sensors on a sensor platform, add a sensor to a sensor platform, remove a sensor from a sensor platform
   
