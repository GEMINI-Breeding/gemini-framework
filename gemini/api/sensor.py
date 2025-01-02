from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.dataset import Dataset
from gemini.api.enums import GEMINISensorType, GEMINIDataType, GEMINIDataFormat

from gemini.db.models.sensors import SensorModel
from gemini.db.models.sensor_types import SensorTypeModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.views.experiment_views import ExperimentSensorsViewModel

class Sensor(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "sensor_id"))

    sensor_name: str
    sensor_type_id: int
    sensor_data_type_id: int
    sensor_data_format_id: int
    sensor_info: Optional[dict] = None

    datasets: List[Dataset]

    @classmethod
    def create(
        cls,
        sensor_name: str,
        sensor_type: GEMINISensorType = GEMINISensorType.Default,
        sensor_data_type: GEMINIDataType = GEMINIDataType.Default,
        sensor_data_format: GEMINIDataFormat = GEMINIDataFormat.Default,
        sensor_info: dict = {}
    ) -> "Sensor":
        try:
            sensor_type_id = sensor_type.value
            sensor_data_format_id = sensor_data_format.value
            sensor_data_type_id = sensor_data_type.value

            db_instance = SensorModel.get_or_create(
                sensor_name=sensor_name,
                sensor_type_id=sensor_type_id,
                sensor_data_type_id=sensor_data_type_id,
                sensor_data_format_id=sensor_data_format_id,
                sensor_info=sensor_info,
            )

            sensor = cls.model_validate(db_instance)
            experiment = ExperimentModel.get_by_parameters(experiment_name="Default")
            if experiment:
                experiment.sensors.append(sensor)

            return sensor
        except Exception as e:
            raise e
        

    @classmethod
    def get(cls, sensor_name: str) -> "Sensor":
        try:
            db_instance = SensorModel.get_by_parameters(
                sensor_name=sensor_name,
            )
            sensor = cls.model_validate(db_instance)
            return sensor
        except Exception as e:
            raise e
        
    
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Sensor":
        try:
            db_instance = SensorModel.get(id)
            sensor = cls.model_validate(db_instance)
            return sensor
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["Sensor"]:
        try:
            sensors = SensorModel.all()
            sensors = [cls.model_validate(sensor) for sensor in sensors]
            return sensors if sensors else None
        except Exception as e:
            raise e
        

    @classmethod
    def search(cls, **search_parameters) -> List["Sensor"]:
        try:
            sensors = ExperimentSensorsViewModel.search(**search_parameters)
            sensors = [cls.model_validate(sensor) for sensor in sensors]
            return sensors if sensors else None
        except Exception as e:
            raise e
        

    def update(self, **update_parameters) -> "Sensor":
        try:
            current_id = self.id
            sensor = SensorModel.get(current_id)
            sensor = SensorModel.update(sensor, **update_parameters)
            sensor = self.model_validate(sensor)
            self.refresh()
            return sensor
        except Exception as e:
            raise e
        

    def delete(self) -> bool:
        try:
            current_id = self.id
            sensor = SensorModel.get(current_id)
            SensorModel.delete(sensor)
            return True
        except Exception as e:
            raise e
        

    def refresh(self) -> "Sensor":
        try:
            db_instance = SensorModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    actual_value = getattr(instance, key)
                    setattr(self, key, actual_value)
            return self
        except Exception as e:
            raise e