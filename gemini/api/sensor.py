from typing import Optional, List
from uuid import UUID
from tqdm import tqdm

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.sensor_record import SensorRecord
from gemini.api.dataset import Dataset, GEMINIDatasetType
from gemini.api.enums import GEMINISensorType, GEMINIDataType, GEMINIDataFormat
from gemini.db.models.sensors import SensorModel
from gemini.db.models.sensor_platforms import SensorPlatformModel
from gemini.db.models.views.experiment_views import ExperimentSensorsViewModel
from gemini.db.models.associations import ExperimentSensorModel, SensorPlatformSensorModel, SensorDatasetModel
from gemini.db.models.views.dataset_views import SensorDatasetsViewModel
from gemini.db.models.views.sensor_platform_sensors_view import SensorPlatformSensorsViewModel
from datetime import date, datetime

class Sensor(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "sensor_id"))

    sensor_name: str
    sensor_type_id: int
    sensor_data_type_id: int
    sensor_data_format_id: int
    sensor_info: Optional[dict] = None

    def __str__(self):
        return f"Sensor(name={self.sensor_name}, id={self.id})"
    
    def __repr__(self):
        return f"Sensor(sensor_name={self.sensor_name}, id={self.id}, sensor_type_id={self.sensor_type_id}, sensor_data_type_id={self.sensor_data_type_id}, sensor_data_format_id={self.sensor_data_format_id})"
    
    @classmethod
    def exists(
        cls,
        sensor_name: str
    ) -> bool:
        try:
            exists = SensorModel.exists(sensor_name=sensor_name)
            return exists
        except Exception as e:
            print(f"Error checking existence of sensor: {e}")
            return False
    
    @classmethod
    def create(
        cls,
        sensor_name: str,
        sensor_type: GEMINISensorType = GEMINISensorType.Default,
        sensor_data_type: GEMINIDataType = GEMINIDataType.Default,
        sensor_data_format: GEMINIDataFormat = GEMINIDataFormat.Default,
        sensor_info: dict = {},
        experiment_name: str = None,
        sensor_platform_name: str = None
    ) -> Optional["Sensor"]:
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
            if experiment_name:
                sensor.associate_experiment(experiment_name=experiment_name)
            if sensor_platform_name:
                sensor.associate_sensor_platform(sensor_platform_name=sensor_platform_name)
            return sensor
        except Exception as e:
            print(f"Error creating sensor: {e}")
            return None
    
    @classmethod
    def get(
        cls,
        sensor_name: str,
        experiment_name: str = None
    ) -> Optional["Sensor"]:
        try:
            db_instance = SensorModel.get_by_parameters(
                sensor_name=sensor_name,
                experiment_name=experiment_name
            )
            if not db_instance:
                print(f"Sensor with name {sensor_name} not found.")
                return None
            sensor = cls.model_validate(db_instance)
            return sensor
        except Exception as e:
            print(f"Error getting sensor: {e}")
            return None
    
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["Sensor"]:
        try:
            db_instance = SensorModel.get(id)
            if not db_instance:
                print(f"Sensor with ID {id} does not exist.")
                return None
            sensor = cls.model_validate(db_instance)
            return sensor
        except Exception as e:
            print(f"Error getting sensor by ID: {e}")
            return None
        
    @classmethod
    def get_all(cls) -> Optional[List["Sensor"]]:
        try:
            sensors = SensorModel.all()
            if not sensors or len(sensors) == 0:
                print("No sensors found.")
                return None
            sensors = [cls.model_validate(sensor) for sensor in sensors]
            return sensors
        except Exception as e:
            print(f"Error getting all sensors: {e}")
            return None
        
    @classmethod
    def search(
        cls,
        sensor_name: str = None,
        sensor_type: GEMINISensorType = None,
        sensor_data_type: GEMINIDataType = None,
        sensor_data_format: GEMINIDataFormat = None,
        sensor_info: dict = None,
        experiment_name: str = None,
        sensor_platform_name: str = None
    ) -> Optional[List["Sensor"]]:
        try:
            if not any([sensor_name, sensor_type, sensor_data_type, sensor_data_format, sensor_info, experiment_name, sensor_platform_name]):
                print("Must provide at least one search parameter.")
                return None
            sensors = ExperimentSensorsViewModel.search(
                sensor_name=sensor_name,
                sensor_type=sensor_type.value if sensor_type else None,
                sensor_data_type=sensor_data_type.value if sensor_data_type else None,
                sensor_data_format=sensor_data_format.value if sensor_data_format else None,
                sensor_info=sensor_info,
                experiment_name=experiment_name,
                sensor_platform_name=sensor_platform_name
            )
            if not sensors or len(sensors) == 0:
                print("No sensors found with the provided search parameters.")
                return None
            sensors = [cls.model_validate(sensor) for sensor in sensors]
            return sensors
        except Exception as e:
            print(f"Error searching sensors: {e}")
            return None
        
    def update(
        self,
        sensor_name: str = None, 
        sensor_type: GEMINISensorType = None,
        sensor_data_type: GEMINIDataType = None,
        sensor_data_format: GEMINIDataFormat = None,
        sensor_info: dict = None
    ) -> Optional["Sensor"]:
        try:
            if not any([sensor_type, sensor_data_type, sensor_data_format, sensor_info, sensor_name]):
                print("At least one update parameter must be provided.")
                return None

            current_id = self.id
            sensor = SensorModel.get(current_id)
            if not sensor:
                print(f"Sensor with ID {current_id} does not exist.")
                return None
            
            sensor = SensorModel.update(
                sensor,
                sensor_name=sensor_name,
                sensor_type_id=sensor_type.value if sensor_type else None,
                sensor_data_type_id=sensor_data_type.value if sensor_data_type else None,
                sensor_data_format_id=sensor_data_format.value if sensor_data_format else None,
                sensor_info=sensor_info
            )
            updated_sensor = self.model_validate(sensor)
            self.refresh()
            return updated_sensor
        except Exception as e:
            print(f"Error updating sensor: {e}")
            return None
    
    def delete(self) -> bool:
        try:
            current_id = self.id
            sensor = SensorModel.get(current_id)
            if not sensor:
                print(f"Sensor with ID {current_id} does not exist.")
                return False
            SensorModel.delete(sensor)
            return True
        except Exception as e:
            print(f"Error deleting sensor: {e}")
            return False
        
    def refresh(self) -> Optional["Sensor"]:
        try:
            db_instance = SensorModel.get(self.id)
            if not db_instance:
                print(f"Sensor with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    actual_value = getattr(instance, key)
                    setattr(self, key, actual_value)
            return self
        except Exception as e:
            print(f"Error refreshing sensor: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            sensor = SensorModel.get(current_id)
            if not sensor:
                print(f"Sensor with ID {current_id} does not exist.")
                return None
            sensor_info = sensor.sensor_info
            if not sensor_info:
                print("Sensor info is empty.")
                return None
            return sensor_info
        except Exception as e:
            print(f"Error getting sensor info: {e}")
            return None
        
    def set_info(self, sensor_info: dict) -> Optional["Sensor"]:
        try:
            current_id = self.id
            sensor = SensorModel.get(current_id)
            if not sensor:
                print(f"Sensor with ID {current_id} does not exist.")
                return None
            sensor = SensorModel.update(
                sensor,
                sensor_info=sensor_info
            )
            sensor = self.model_validate(sensor)
            self.refresh()
            return sensor
        except Exception as e:
            print(f"Error setting sensor info: {e}")
            return None
        
    def get_associated_sensor_platforms(self):
        try:
            from gemini.api.sensor_platform import SensorPlatform
            sensor_platforms = SensorPlatformSensorsViewModel.search(sensor_id=self.id)
            if not sensor_platforms or len(sensor_platforms) == 0:
                print("No associated sensor platforms found.")
                return None
            sensor_platforms = [SensorPlatform.model_validate(sensor_platform) for sensor_platform in sensor_platforms]
            return sensor_platforms
        except Exception as e:
            print(f"Error getting associated sensor platforms: {e}")
            return None

    def associate_sensor_platform(self, sensor_platform_name: str):
        try:
            from gemini.api.sensor_platform import SensorPlatform
            sensor_platform = SensorPlatform.get(sensor_platform_name=sensor_platform_name)
            if not sensor_platform:
                print(f"Sensor platform {sensor_platform_name} does not exist.")
                return None
            existing_association = SensorPlatformSensorModel.get_by_parameters(
                sensor_platform_id=sensor_platform.id,
                sensor_id=self.id
            )
            if existing_association:
                print(f"Sensor {self.sensor_name} already associated with sensor platform {sensor_platform_name}.")
                return None
            new_association = SensorPlatformSensorModel.get_or_create(
                sensor_platform_id=sensor_platform.id,
                sensor_id=self.id
            )
            if not new_association:
                print(f"Failed to associate sensor {self.sensor_name} with sensor platform {sensor_platform_name}.")
                return None
            self.refresh()
            return sensor_platform
        except Exception as e:
            print(f"Error associating sensor platform: {e}")
            return None

    def unassociate_sensor_platform(self, sensor_platform_name: str):
        try:
            from gemini.api.sensor_platform import SensorPlatform
            sensor_platform = SensorPlatform.get(sensor_platform_name=sensor_platform_name)
            if not sensor_platform:
                print(f"Sensor platform {sensor_platform_name} does not exist.")
                return None
            existing_association = SensorPlatformSensorModel.get_by_parameters(
                sensor_platform_id=sensor_platform.id,
                sensor_id=self.id
            )
            if not existing_association:
                print(f"Sensor {self.sensor_name} not associated with sensor platform {sensor_platform_name}.")
                return None
            is_deleted = SensorPlatformSensorModel.delete(existing_association)
            if not is_deleted:
                print(f"Failed to unassociate sensor {self.sensor_name} from sensor platform {sensor_platform_name}.")
                return None
            self.refresh()
            return sensor_platform
        except Exception as e:
            print(f"Error unassociating sensor platform: {e}")
            return None

    def belongs_to_sensor_platform(self, sensor_platform_name: str) -> bool:
        try:
            from gemini.api.sensor_platform import SensorPlatform
            sensor_platform = SensorPlatform.get(sensor_platform_name=sensor_platform_name)
            if not sensor_platform:
                print(f"Sensor platform {sensor_platform_name} does not exist.")
                return False
            association_exists = SensorPlatformSensorModel.exists(
                sensor_platform_id=sensor_platform.id,
                sensor_id=self.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking sensor platform membership: {e}")
            return

    def get_associated_experiments(self):
        try:
            from gemini.api.experiment import Experiment
            experiments = ExperimentSensorsViewModel.search(sensor_id=self.id)
            if not experiments or len(experiments) == 0:
                print("No associated experiments found.")
                return None
            experiments = [Experiment.model_validate(experiment) for experiment in experiments]
            return experiments
        except Exception as e:
            print(f"Error getting associated experiments: {e}")
            return None

    def associate_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return None
            existing_association = ExperimentSensorModel.get_by_parameters(
                experiment_id=experiment.id,
                sensor_id=self.id
            )
            if existing_association:
                print(f"Sensor {self.sensor_name} already associated with experiment {experiment_name}.")
                return None
            new_association = ExperimentSensorModel.get_or_create(
                experiment_id=experiment.id,
                sensor_id=self.id
            )
            if not new_association:
                print(f"Failed to associate sensor {self.sensor_name} with experiment {experiment_name}.")
                return None
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error associating experiment: {e}")
            return None

    def unassociate_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return None
            existing_association = ExperimentSensorModel.get_by_parameters(
                experiment_id=experiment.id,
                sensor_id=self.id
            )
            if not existing_association:
                print(f"Sensor {self.sensor_name} not associated with experiment {experiment_name}.")
                return None
            is_deleted = ExperimentSensorModel.delete(existing_association)
            if not is_deleted:
                print(f"Failed to unassociate sensor {self.sensor_name} from experiment {experiment_name}.")
                return None
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error unassociating experiment: {e}")
            return None

    def belongs_to_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return False
            association_exists = ExperimentSensorModel.exists(
                experiment_id=experiment.id,
                sensor_id=self.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking experiment membership: {e}")
            return False

    def get_associated_datasets(self):
        try:
            datasets = SensorDatasetsViewModel.search(sensor_id=self.id)
            if not datasets or len(datasets) == 0:
                print("No associated datasets found.")
                return None
            datasets = [Dataset.model_validate(dataset) for dataset in datasets]
            return datasets
        except Exception as e:
            print(f"Error getting associated datasets: {e}")
            return None

    def create_new_dataset(
        self,
        dataset_name: str,
        dataset_info: dict = {},
        collection_date: date = None,
        experiment_name: str = None
    ):
        try:
            from gemini.api.dataset import Dataset
            dataset = Dataset.create(
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                collection_date=collection_date,
                experiment_name=experiment_name,
                dataset_type=GEMINIDatasetType.Sensor
            )
            if not dataset:
                print("Failed to create new dataset.")
                return None
            dataset = self.associate_dataset(dataset_name=dataset.dataset_name)
            return dataset
        except Exception as e:
            print(f"Error creating new dataset: {e}")
            return None
        
    def associate_dataset(self, dataset_name: str):
        try:
            from gemini.api.dataset import Dataset
            dataset = Dataset.get(dataset_name=dataset_name)
            if not dataset:
                print(f"Dataset {dataset_name} does not exist.")
                return None
            existing_association = SensorDatasetModel.get_by_parameters(
                dataset_id=dataset.id,
                sensor_id=self.id
            )
            if existing_association:
                print(f"Sensor {self.sensor_name} already associated with dataset {dataset_name}.")
                return None
            new_association = SensorDatasetModel.get_or_create(
                dataset_id=dataset.id,
                sensor_id=self.id
            )
            if not new_association:
                print(f"Failed to associate sensor {self.sensor_name} with dataset {dataset_name}.")
                return None
            self.refresh()
            return dataset
        except Exception as e:
            print(f"Error associating dataset: {e}")
            return None
        
    def insert_record(
        self,
        timestamp: datetime = None,
        collection_date: date = None,
        dataset_name: str = None,
        sensor_data: dict = {},
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        plot_number: int = -1,
        plot_row_number: int = -1,
        plot_column_number: int = -1,
        record_file: str = None,
        record_info: dict = {}
    ) -> tuple[bool, List[str]]:
        try:
            if not experiment_name or not season_name or not site_name:
                raise ValueError("Experiment name, season name, and site name must be provided.")
            
            if not sensor_data and not record_file:
                raise ValueError("Either sensor_data or record_file must be provided.")
            
            timestamp = timestamp if timestamp else datetime.now()
            collection_date = collection_date if collection_date else timestamp.date()
            sensor_name = self.sensor_name

            if not dataset_name:
                dataset_name = f"{sensor_name} Dataset {collection_date}"

            sensor_record = SensorRecord.create(
                timestamp=timestamp,
                collection_date=collection_date,
                sensor_name=sensor_name,
                sensor_data=sensor_data,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                plot_number=plot_number if plot_number != -1 else None,
                plot_row_number=plot_row_number if plot_row_number != -1 else None,
                plot_column_number=plot_column_number if plot_column_number != -1 else None,
                record_file=record_file if record_file else None,
                record_info=record_info if record_info else {},
                insert_on_create=False
            )
            success, inserted_record_ids = SensorRecord.insert([sensor_record])
            if not success:
                print("Failed to insert sensor record.")
                return False, []
            return success, inserted_record_ids
        except Exception as e:
            print(f"Error inserting sensor record: {e}")
            return False, []
        
    def insert_records(
        self,
        timestamps: List[datetime] = None,
        collection_date: date = None,
        sensor_data: List[dict] = [],
        dataset_name: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        plot_numbers: List[int] = None,
        plot_row_numbers: List[int] = None,
        plot_column_numbers: List[int] = None,
        record_files: List[str] = None,
        record_info: List[dict] = []
    ) -> tuple[bool, List[str]]:
        try:
            if not experiment_name or not season_name or not site_name:
                raise ValueError("Experiment name, season name, and site name must be provided.")
            
            if len(timestamps) == 0:
                raise ValueError("At least one timestamp must be provided.")
            
            if not dataset_name:
                dataset_name = f"{self.sensor_name} Dataset {collection_date}"

            collection_date = collection_date if collection_date else timestamps[0].date()
            sensor_records = []
            timestamps_length = len(timestamps)

            for i in tqdm(range(timestamps_length), desc="Arranging Records for Sensor: " + self.sensor_name):
                sensor_record = SensorRecord.create(
                    timestamp=timestamps[i],
                    collection_date=collection_date,
                    sensor_name=self.sensor_name,
                    sensor_data=sensor_data[i] if sensor_data else {},
                    experiment_name=experiment_name,
                    dataset_name=dataset_name if dataset_name else f"{self.sensor_name} Dataset",
                    season_name=season_name,
                    site_name=site_name,
                    plot_number=plot_numbers[i] if plot_numbers else None,
                    plot_row_number=plot_row_numbers[i] if plot_row_numbers else None,
                    plot_column_number=plot_column_numbers[i] if plot_column_numbers else None,
                    record_file=record_files[i] if record_files else None,
                    record_info=record_info[i] if record_info else {},
                    insert_on_create=False
                )
                sensor_records.append(sensor_record)

            success, inserted_record_ids = SensorRecord.insert(sensor_records)
            return success, inserted_record_ids
        except Exception as e:
            print(f"Error inserting sensor records: {e}")
            return False, []
        
    def search_records(
        self,
        collection_date: date = None,
        dataset_name: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
        record_info: dict = None
    ) -> List[SensorRecord]:
        try:
            record_info = record_info if record_info else {}
            record_info = {k: v for k, v in record_info.items() if v is not None}

            records = SensorRecord.search(
                sensor_name=self.sensor_name,
                collection_date=collection_date,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                record_info=record_info
            )
            return records
        except Exception as e:
            print(f"Error searching sensor records: {e}")
            return []


    
     