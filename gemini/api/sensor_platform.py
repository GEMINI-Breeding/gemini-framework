from typing import List, Optional
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.sensor import Sensor, GEMINIDataFormat, GEMINIDataType, GEMINISensorType
from gemini.db.models.associations import ExperimentSensorPlatformModel, SensorPlatformSensorModel
from gemini.db.models.sensor_platforms import SensorPlatformModel
from gemini.db.models.views.experiment_views import ExperimentSensorPlatformsViewModel
from gemini.db.models.views.sensor_platform_sensors_view import SensorPlatformSensorsViewModel

class SensorPlatform(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "sensor_platform_id"))

    sensor_platform_name: str
    sensor_platform_info: Optional[dict] = None

    def __str__(self):
        return f"SensorPlatform(id={self.id}, name={self.sensor_platform_name})"
    
    def __repr__(self):
        return f"SensorPlatform(id={self.id}, name={self.sensor_platform_name})"
    
    @classmethod
    def exists(
        cls,
        sensor_platform_name: str,
    ) -> bool:
        try:
            exists = SensorPlatformModel.exists(sensor_platform_name=sensor_platform_name)
            return exists
        except Exception as e:
            print(f"Error checking existence of SensorPlatform: {e}")
            return False
    
    @classmethod
    def create(
        cls,
        sensor_platform_name: str,
        sensor_platform_info: dict = {},
        experiment_name: str = None
    ) -> Optional["SensorPlatform"]:
        try:
            db_instance = SensorPlatformModel.get_or_create(
                sensor_platform_name=sensor_platform_name,
                sensor_platform_info=sensor_platform_info,
            )
            sensor_platform = cls.model_validate(db_instance)
            if experiment_name:
                sensor_platform.associate_experiment(experiment_name=experiment_name)
            return sensor_platform
        except Exception as e:
            print(f"Error creating SensorPlatform: {e}")
            return None
        
    @classmethod
    def get(
        cls,
        sensor_platform_name: str,
        experiment_name: str = None
    ) -> Optional["SensorPlatform"]:
        try:
            db_instance = ExperimentSensorPlatformsViewModel.get_by_parameters(
                sensor_platform_name=sensor_platform_name,
                experiment_name=experiment_name
            )
            if not db_instance:
                print(f"SensorPlatform with name {sensor_platform_name} not found.")
                return None
            sensor_platform = cls.model_validate(db_instance)
            return sensor_platform
        except Exception as e:
            print(f"Error retrieving SensorPlatform: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["SensorPlatform"]:
        try:
            db_instance = SensorPlatformModel.get(id)
            if not db_instance:
                print(f"SensorPlatform with ID {id} not found.")
                return None
            sensor_platform = cls.model_validate(db_instance)
            return sensor_platform
        except Exception as e:
            print(f"Error retrieving SensorPlatform by ID: {e}")
            return None
        
    @classmethod
    def get_all(cls) -> Optional[List["SensorPlatform"]]:
        try:
            sensor_platforms = SensorPlatformModel.all()
            if not sensor_platforms or len(sensor_platforms) == 0:
                print("No SensorPlatforms found.")
                return None
            sensor_platforms = [cls.model_validate(sp) for sp in sensor_platforms]
            return sensor_platforms
        except Exception as e:
            print(f"Error retrieving all SensorPlatforms: {e}")
            return None
        
    @classmethod
    def search(
        cls,
        sensor_platform_name: str = None,
        sensor_platform_info: dict = None,
        experiment_name: str = None
    ) -> Optional[List["SensorPlatform"]]:
        try:
            if not any([sensor_platform_name, sensor_platform_info, experiment_name]):
                print("At least one search parameter must be provided.")
                return None
            instances = ExperimentSensorPlatformsViewModel.search(
                sensor_platform_name=sensor_platform_name,
                sensor_platform_info=sensor_platform_info,
                experiment_name=experiment_name
            )
            if not instances or len(instances) == 0:
                print("No SensorPlatforms found matching the search criteria.")
                return None
            sensor_platforms = [cls.model_validate(instance) for instance in instances]
            return sensor_platforms
        except Exception as e:
            print(f"Error searching SensorPlatforms: {e}")
            return None
        
    def update(
        self,
        sensor_platform_name: str = None,
        sensor_platform_info: dict = None
    ) -> Optional["SensorPlatform"]:
        try:
            if not any([sensor_platform_name, sensor_platform_info]):
                print("At least one update parameter must be provided.")
                return None
            current_id = self.id
            platform = SensorPlatformModel.get(current_id)
            if not platform:
                print(f"SensorPlatform with ID {current_id} not found.")
                return None
            platform = SensorPlatformModel.update(
                platform, 
                sensor_platform_info=sensor_platform_info,
                sensor_platform_name=sensor_platform_name
            )
            platform = self.model_validate(platform)
            self.refresh()
            return platform
        except Exception as e:
            print(f"Error updating SensorPlatform: {e}")
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            platform = SensorPlatformModel.get(current_id)
            if not platform:
                print(f"SensorPlatform with ID {current_id} not found.")
                return False
            SensorPlatformModel.delete(platform)
            return True
        except Exception as e:
            print(f"Error deleting SensorPlatform: {e}")
            return False
        
    def refresh(self) -> Optional["SensorPlatform"]:
        try:
            db_instance = SensorPlatformModel.get(self.id)
            if not db_instance:
                print(f"SensorPlatform with ID {self.id} not found.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing SensorPlatform: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            sensor_platform = SensorPlatformModel.get(current_id)
            if not sensor_platform:
                print(f"SensorPlatform with ID {current_id} not found.")
                return None
            sensor_platform_info = sensor_platform.sensor_platform_info
            if not sensor_platform_info:
                print("SensorPlatform info is empty.")
                return None
            return sensor_platform_info
        except Exception as e:
            print(f"Error retrieving SensorPlatform info: {e}")
            return None
        
    def set_info(self, sensor_platform_info: dict) -> Optional["SensorPlatform"]:
        try:
            current_id = self.id
            sensor_platform = SensorPlatformModel.get(current_id)
            if not sensor_platform:
                print(f"SensorPlatform with ID {current_id} not found.")
                return None
            sensor_platform = SensorPlatformModel.update(
                sensor_platform,
                sensor_platform_info=sensor_platform_info
            )
            sensor_platform = self.model_validate(sensor_platform)
            self.refresh()
            return self
        except Exception as e:
            print(f"Error setting SensorPlatform info: {e}")
            return None
            
    def get_associated_sensors(self):
        try:
            from gemini.api.sensor import Sensor
            sensor_platform_sensors = SensorPlatformSensorsViewModel.search(
                sensor_platform_id=self.id
            )
            if not sensor_platform_sensors or len(sensor_platform_sensors) == 0:
                print(f"No sensors found for SensorPlatform {self.sensor_platform_name}.")
                return None
            sensors = [Sensor.model_validate(sensor) for sensor in sensor_platform_sensors]
            return sensors
        except Exception as e:
            print(f"Error retrieving sensors for SensorPlatform: {e}")
            return None

    def create_new_sensor(
        self,
        sensor_name: str,
        sensor_type: GEMINISensorType = GEMINISensorType.Default,
        sensor_data_type: GEMINIDataType = GEMINIDataType.Default,
        sensor_data_format: GEMINIDataFormat = GEMINIDataFormat.Default,
        sensor_info: dict = {},
        experiment_name: str = None
    ):
        try:
            from gemini.api.sensor import Sensor
            new_sensor = Sensor.create(
                sensor_name=sensor_name,
                sensor_type=sensor_type,
                sensor_data_type=sensor_data_type,
                sensor_data_format=sensor_data_format,
                sensor_info=sensor_info,
                experiment_name=experiment_name,
                sensor_platform_name=self.sensor_platform_name
            )
            if not new_sensor:
                print(f"Failed to create sensor {sensor_name}.")
                return None
            return new_sensor
        except Exception as e:
            print(f"Error creating new sensor for SensorPlatform: {e}")
            return None

    def associate_sensor(self, sensor_name: str):
        try:
            from gemini.api.sensor import Sensor
            sensor = Sensor.get(sensor_name=sensor_name)
            if not sensor:
                print(f"Sensor {sensor_name} not found.")
                return None
            existing_association = SensorPlatformSensorModel.exists(
                sensor_platform_id=self.id,
                sensor_id=sensor.id
            )
            if existing_association:
                print(f"Sensor {sensor_name} is already associated with SensorPlatform {self.sensor_platform_name}.")
                return None
            new_association = SensorPlatformSensorModel.create(
                sensor_platform_id=self.id,
                sensor_id=sensor.id
            )
            self.refresh()
            return sensor
        except Exception as e:
            print(f"Error associating sensor {sensor_name} with SensorPlatform: {e}")
            return None

    def unassociate_sensor(self, sensor_name: str):
        try:
            from gemini.api.sensor import Sensor
            sensor = Sensor.get(sensor_name=sensor_name)
            if not sensor:
                print(f"Sensor {self.sensor_platform_name} not found.")
                return None
            existing_association = SensorPlatformSensorModel.get_by_parameters(
                sensor_platform_id=self.id,
                sensor_id=sensor.id
            )
            if not existing_association:
                print(f"Sensor {self.sensor_platform_name} is not associated with SensorPlatform {self.sensor_platform_name}.")
                return None
            is_deleted = SensorPlatformSensorModel.delete(existing_association)
            if not is_deleted:
                print(f"Failed to unassociate sensor {self.sensor_platform_name} from SensorPlatform {self.sensor_platform_name}.")
                return None
            self.refresh()
            return sensor
        except Exception as e:
            print(f"Error unassociating sensor {self.sensor_platform_name} from SensorPlatform: {e}")
            return None

    def belongs_to_sensor(self, sensor_name: str) -> bool:
        try:
            from gemini.api.sensor import Sensor
            sensor = Sensor.get(sensor_name=sensor_name)
            if not sensor:
                print(f"Sensor {sensor_name} not found.")
                return False
            association_exists = SensorPlatformSensorModel.exists(
                sensor_platform_id=self.id,
                sensor_id=sensor.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking if SensorPlatform belongs to sensor {sensor_name}: {e}")
            return False

    def get_associated_experiments(self):
        try:
            from gemini.api.experiment import Experiment
            experiment_sensor_platforms = ExperimentSensorPlatformsViewModel.search(
                sensor_platform_id=self.id
            )
            if not experiment_sensor_platforms or len(experiment_sensor_platforms) == 0:
                print(f"No experiments found for SensorPlatform {self.sensor_platform_name}.")
                return None
            experiments = [Experiment.model_validate(exp) for exp in experiment_sensor_platforms]
            return experiments
        except Exception as e:
            print(f"Error retrieving associated experiments for SensorPlatform: {e}")
            return None

    def associate_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} not found.")
                return None
            existing_association = ExperimentSensorPlatformModel.exists(
                sensor_platform_id=self.id,
                experiment_id=experiment.id
            )
            if existing_association:
                print(f"Experiment {experiment_name} is already associated with SensorPlatform {self.sensor_platform_name}.")
                return None
            new_association = ExperimentSensorPlatformModel.create(
                sensor_platform_id=self.id,
                experiment_id=experiment.id
            )
            if not new_association:
                print(f"Failed to associate Experiment {experiment_name} with SensorPlatform {self.sensor_platform_name}.")
                return None
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error associating Experiment {experiment_name} with SensorPlatform: {e}")
            return None

    def unassociate_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} not found.")
                return None
            existing_association = ExperimentSensorPlatformModel.get_by_parameters(
                sensor_platform_id=self.id,
                experiment_id=experiment.id
            )
            if not existing_association:
                print(f"Experiment {experiment_name} is not associated with SensorPlatform {self.sensor_platform_name}.")
                return None
            is_deleted = ExperimentSensorPlatformModel.delete(existing_association)
            if not is_deleted:
                print(f"Failed to unassociate Experiment {experiment_name} from SensorPlatform {self.sensor_platform_name}.")
                return None
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error unassociating Experiment {experiment_name} from SensorPlatform: {e}")
            return None

    def belongs_to_experiment(self, experiment_name: str) -> bool:
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment {self.sensor_platform_name} not found.")
                return False
            association_exists = ExperimentSensorPlatformModel.exists(
                sensor_platform_id=self.id,
                experiment_id=experiment.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking if SensorPlatform belongs to experiment {self.sensor_platform_name}: {e}")
            return False

    