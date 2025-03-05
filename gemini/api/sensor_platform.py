from typing import List, Optional
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.sensor import Sensor, GEMINIDataFormat, GEMINIDataType, GEMINISensorType
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.associations import ExperimentSensorPlatformModel, SensorPlatformSensorModel
from gemini.db.models.sensor_platforms import SensorPlatformModel
from gemini.db.models.views.experiment_views import ExperimentSensorPlatformsViewModel

class SensorPlatform(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "sensor_platform_id"))

    sensor_platform_name: str
    sensor_platform_info: Optional[dict] = None


    @classmethod
    def create(
        cls,
        sensor_platform_name: str,
        sensor_platform_info: dict = {},
        experiment_name: str = None
    ) -> "SensorPlatform":
        try:
            db_instance = SensorPlatformModel.get_or_create(
                sensor_platform_name=sensor_platform_name,
                sensor_platform_info=sensor_platform_info,
            )

            if experiment_name:
                db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
                if db_experiment:
                    ExperimentSensorPlatformModel.get_or_create(experiment_id=db_experiment.id, sensor_platform_id=db_instance.id)

            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            raise e
    
    @classmethod
    def get(cls, sensor_platform_name: str, experiment_name: str = None) -> "SensorPlatform":
        try:

            instance = ExperimentSensorPlatformsViewModel.get_by_parameters(
                sensor_platform_name=sensor_platform_name,
                experiment_name=experiment_name
            )
            instance = cls.model_validate(instance)
            return instance if instance else None
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "SensorPlatform":
        try:
            instance = SensorPlatformModel.get(id)
            instance = cls.model_validate(instance)
            return instance if instance else None
        except Exception as e:
            raise e
        
    @classmethod
    def get_all(cls) -> List["SensorPlatform"]:
        try:
            instances = SensorPlatformModel.all()
            instances = [cls.model_validate(instance) for instance in instances]
            return instances if instances else None
        except Exception as e:
            raise e
        

    @classmethod
    def search(
        cls, 
        experiment_name: str = None,
        sensor_platform_name: str = None,
        sensor_platform_info: dict = None
    ) -> List["SensorPlatform"]:
        try:
            if not any([experiment_name, sensor_platform_name, sensor_platform_info]):
                raise ValueError("At least one search parameter must be provided.")

            instances = ExperimentSensorPlatformsViewModel.search(
                experiment_name=experiment_name,
                sensor_platform_name=sensor_platform_name,
                sensor_platform_info=sensor_platform_info
            )
            instances = [cls.model_validate(instance) for instance in instances]
            return instances if instances else None
        except Exception as e:
            raise e
        

    def update(
            self,
            sensor_platform_name: str = None, 
            sensor_platform_info: dict = None
        ) -> "SensorPlatform":
        try:
            if not sensor_platform_info and not sensor_platform_name:
                raise ValueError("At least one update parameter must be provided.")

            current_id = self.id
            platform = SensorPlatformModel.get(current_id)
            platform = SensorPlatformModel.update(
                platform, 
                sensor_platform_info=sensor_platform_info,
                sensor_platform_name=sensor_platform_name
            )
            platform = self.model_validate(platform)
            self.refresh()
            return platform
        except Exception as e:
            raise e
        

    def delete(self) -> bool:
        try:
            current_id = self.id
            platform = SensorPlatformModel.get(current_id)
            SensorPlatformModel.delete(platform)
            return True
        except Exception as e:
            return False
        

    def refresh(self) -> "SensorPlatform":
        try:
            db_instance = SensorPlatformModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e
        

    def get_sensors(self) -> List[Sensor]:
        try:
            sensor_platform = SensorPlatformModel.get(self.id)
            sensors = Sensor.search(sensor_platform_name=sensor_platform.sensor_platform_name)
            return sensors if sensors else None
        except Exception as e:
            raise e
        
    def add_sensor(
        self,
        sensor_name: str,
        sensor_type: GEMINISensorType = GEMINISensorType.Default,
        sensor_data_type: GEMINIDataType = GEMINIDataType.Default,
        sensor_data_format: GEMINIDataFormat = GEMINIDataFormat.Default,
        sensor_info: dict = {},
        experiment_name: str = None
    ) -> "Sensor":
        try:
            sensor = Sensor.create(
                sensor_name=sensor_name,
                sensor_type=sensor_type,
                sensor_data_type=sensor_data_type,
                sensor_data_format=sensor_data_format,
                sensor_info=sensor_info,
                sensor_platform_name=self.sensor_platform_name,
                experiment_name=experiment_name
            )
            SensorPlatformSensorModel.get_or_create(
                sensor_platform_id=self.id,
                sensor_id=sensor.id
            )
            return sensor
        except Exception as e:
            raise e
            
        