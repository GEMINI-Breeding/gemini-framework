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
from gemini.db.models.sensor_types import SensorTypeModel
from gemini.db.models.sensor_platforms import SensorPlatformModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.views.experiment_views import ExperimentSensorsViewModel
from gemini.db.models.associations import ExperimentSensorModel, SensorPlatformSensorModel, SensorDatasetModel
from gemini.db.models.views.dataset_views import SensorDatasetsViewModel
from datetime import date, datetime

class Sensor(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "sensor_id"))

    sensor_name: str
    sensor_type_id: int
    sensor_data_type_id: int
    sensor_data_format_id: int
    sensor_info: Optional[dict] = None

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

            if experiment_name:
                db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
                if db_experiment:
                    ExperimentSensorModel.get_or_create(experiment_id=db_experiment.id, sensor_id=db_instance.id)

            if sensor_platform_name:
                db_sensor_platform = SensorPlatformModel.get_by_parameters(sensor_platform_name=sensor_platform_name)
                if db_sensor_platform:
                    SensorPlatformSensorModel.get_or_create(sensor_id=db_instance.id, sensor_platform_id=db_sensor_platform.id)

            sensor = cls.model_validate(db_instance)
            return sensor
        except Exception as e:
            raise e
        

    @classmethod
    def get(cls, sensor_name: str, experiment_name: str = None) -> "Sensor":
        try:
            db_instance = SensorModel.get_by_parameters(
                sensor_name=sensor_name,
                experiment_name=experiment_name
            )
            sensor = cls.model_validate(db_instance)
            return sensor if sensor else None
        except Exception as e:
            raise e
        
    
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Sensor":
        try:
            db_instance = SensorModel.get(id)
            sensor = cls.model_validate(db_instance)
            return sensor if sensor else None
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
    def search(
        cls,
        experiment_name: str = None,
        sensor_name: str = None,
        sensor_type: GEMINISensorType = None,
        sensor_data_type: GEMINIDataType = None,
        sensor_data_format: GEMINIDataFormat = None,
        sensor_info: dict = None,
        sensor_platform_name: str = None
    ) -> List["Sensor"]:
        try:
            if not any([experiment_name, sensor_name, sensor_type, sensor_data_type, sensor_data_format, sensor_info, sensor_platform_name]):
                raise Exception("Must provide at least one search parameter.")

            sensors = ExperimentSensorsViewModel.search(
                experiment_name=experiment_name,
                sensor_name=sensor_name,
                sensor_type=sensor_type.value if sensor_type else None,
                sensor_data_type=sensor_data_type.value if sensor_data_type else None,
                sensor_data_format=sensor_data_format.value if sensor_data_format else None,
                sensor_info=sensor_info,
                sensor_platform_name=sensor_platform_name
            )
            sensors = [cls.model_validate(sensor) for sensor in sensors]
            return sensors if sensors else None
        except Exception as e:
            raise e
        
    def update(
        self,
        sensor_name: str = None, 
        sensor_type: GEMINISensorType = None,
        sensor_data_type: GEMINIDataType = None,
        sensor_data_format: GEMINIDataFormat = None,
        sensor_info: dict = None
    ) -> "Sensor":
        try:
            if not any([sensor_type, sensor_data_type, sensor_data_format, sensor_info, sensor_name]):
                raise Exception("At least one update parameter must be provided.")

            current_id = self.id
            sensor = SensorModel.get(current_id)
            sensor = SensorModel.update(
                sensor,
                sensor_name=sensor_name,
                sensor_type_id=sensor_type.value if sensor_type else None,
                sensor_data_type_id=sensor_data_type.value if sensor_data_type else None,
                sensor_data_format_id=sensor_data_format.value if sensor_data_format else None,
                sensor_info=sensor_info
            )
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
        
    def get_datasets(self) -> List[Dataset]:
        try:
            sensor = SensorModel.get(self.id)
            datasets = SensorDatasetsViewModel.search(sensor_id=sensor.id)
            datasets = [Dataset.model_validate(dataset) for dataset in datasets]
            return datasets if datasets else None
        except Exception as e:
            raise e
        
    def create_dataset(
        self,
        dataset_name: str,
        dataset_info: dict = {},
        collection_date: date = None,
        experiment_name: str = None
    ) -> Dataset:
        try:
            dataset = Dataset.create(
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                collection_date=collection_date,
                experiment_name=experiment_name,
                dataset_type=GEMINIDatasetType.Sensor
            )
            SensorDatasetModel.get_or_create(sensor_id=self.id, dataset_id=dataset.id)
            return dataset 
        except Exception as e:
            raise e
        
    def add_record(
        self,
        timestamp: date = None,
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
            
            timestamp = timestamp if timestamp else datetime.now()
            collection_date = collection_date if collection_date else timestamp.date()
            sensor_name = self.sensor_name
            sensor_id = self.id

            if not dataset_name:
                dataset_name = sensor_name.lower().replace(" ", "_")
                dataset_name = dataset_name + f"_{collection_date}"
                dataset_name = dataset_name + f"_{experiment_name}_{season_name}_{site_name}"

            sensor_record = SensorRecord(
                timestamp=timestamp,
                collection_date=collection_date,
                sensor_id=sensor_id,
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
                record_info=record_info if record_info else {}
            )
            success, inserted_record_ids = SensorRecord.add([sensor_record])
            return success, inserted_record_ids
        except Exception as e:
            return False, []
        
    def add_records(
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
                dataset_name = self.sensor_name.lower().replace(" ", "_")
                dataset_name = dataset_name + f"_{collection_date}"
                dataset_name = dataset_name + f"_{experiment_name}_{season_name}_{site_name}"

            collection_date = collection_date if collection_date else timestamps[0].date()
            sensor_records = []
            timestamps_length = len(timestamps)

            for i in tqdm(range(timestamps_length), desc="Arranging Records for Sensor: " + self.sensor_name):
                sensor_record = SensorRecord(
                    timestamp=timestamps[i],
                    collection_date=collection_date,
                    sensor_id=self.id,
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
                    record_info=record_info[i] if record_info else {}
                )
                sensor_records.append(sensor_record)

            success, inserted_record_ids = SensorRecord.add(sensor_records)
            return success, inserted_record_ids
        except Exception as e:
            return False, []

    def get_records(
        self,
        collection_date: date = None,
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
            raise e
