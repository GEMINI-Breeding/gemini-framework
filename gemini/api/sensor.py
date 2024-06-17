from typing import Optional, List, Any, Union
from gemini.api.base import APIBase
from gemini.api.sensor_type import SensorType
from gemini.api.data_type import DataType
from gemini.api.data_format import DataFormat
from gemini.api.dataset import Dataset
from gemini.api.sensor_platform import SensorPlatform
from gemini.api.sensor_record import SensorRecord
from gemini.models import SensorModel, ExperimentModel, SensorPlatformModel, DatasetModel
from gemini.models import ExperimentSensorsViewModel
from gemini.logger import logger_service
from gemini.api.enums import GEMINIDataFormat, GEMINIDataType, GEMINISensorType

from uuid import UUID
from datetime import date, datetime
from rich.progress import track

class Sensor(APIBase):

    db_model = SensorModel

    sensor_name: str
    sensor_info: Optional[dict] = None
    sensor_platform_id: Optional[Union[int, str, UUID]] = None
    sensor_type_id: Optional[int] = None
    sensor_data_type_id: Optional[int] = None
    sensor_data_format_id: Optional[int] = None
    
    sensor_type: Optional[SensorType] = None
    data_type: Optional[DataType] = None
    data_format: Optional[DataFormat] = None
    sensor_platform: Optional[SensorPlatform] = None
    datasets: Optional[List[Dataset]] = None

    @classmethod
    def create(
        cls,
        sensor_name: str = 'Default',
        sensor_info: dict = {},
        sensor_platform_name: str = 'Default',
        sensor_type: GEMINISensorType = GEMINIDataFormat.Default,
        sensor_data_type: GEMINIDataType = GEMINIDataType.Default,
        sensor_data_format: GEMINIDataFormat = GEMINIDataFormat.Default,
        experiment_name: str = 'Default'
    ):
        
        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        db_sensor_platform = SensorPlatformModel.get_by_parameters(sensor_platform_name=sensor_platform_name)

        db_instance = cls.db_model.get_or_create(
            sensor_name=sensor_name,
            sensor_info=sensor_info,
            sensor_platform_id=db_sensor_platform.id if db_sensor_platform else None,
            sensor_type_id=sensor_type.value,
            sensor_data_type_id=sensor_data_type.value,
            sensor_data_format_id=sensor_data_format.value
        )

        if db_experiment and db_instance not in db_experiment.sensors:
            db_experiment.sensors.append(db_instance)
            db_experiment.save()

        instance = cls.model_validate(db_instance)
        logger_service.info(
            "API",
            f"Created a new instance of {cls.__name__} with id {instance.id}",
        )
        return instance
    
    @classmethod
    def get(cls, sensor_name: str) -> "Sensor":
        db_instance = cls.db_model.get_by_parameters(sensor_name=sensor_name)
        logger_service.info("API", f"Retrieved sensor with name {sensor_name} from the database")
        return cls.model_validate(db_instance) if db_instance else None
    
    @classmethod
    def get_by_experiment(cls, experiment_name: str) -> List["Sensor"]:
        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        db_sensors = db_experiment.sensors
        logger_service.info("API", f"Retrieved sensors for experiment {experiment_name} from the database")
        return [cls.model_validate(db_sensor) for db_sensor in db_sensors] if db_sensors else None
    
    @classmethod
    def get_by_type(cls, sensor_type: GEMINISensorType) -> List["Sensor"]:
        db_sensors = SensorModel.get_by_parameters(sensor_type_id=sensor_type.value)
        logger_service.info("API", f"Retrieved sensors of type {sensor_type.name} from the database")
        return [cls.model_validate(db_sensor) for db_sensor in db_sensors] if db_sensors else None
    
    def get_by_platform(cls, sensor_platform_name: str) -> List["Sensor"]:
        db_sensor_platform = SensorPlatformModel.get_by_parameters(sensor_platform_name=sensor_platform_name)
        db_sensors = SensorModel.get_by_parameters(sensor_platform_id=db_sensor_platform.id)
        logger_service.info("API", f"Retrieved sensors for platform {sensor_platform_name} from the database")
        return [cls.model_validate(db_sensor) for db_sensor in db_sensors] if db_sensors else None
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.sensor_name} from the database")
        return self.sensor_info
    
    def set_info(self, sensor_info: Optional[dict] = None) -> "Sensor":
        self.update(sensor_info=sensor_info)
        logger_service.info("API", f"Set information about {self.sensor_name} in the database")
        return self
    
    def add_info(self, sensor_info: Optional[dict] = None) -> "Sensor":
        current_info = self.get_info()
        updated_info = {**current_info, **sensor_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information to {self.sensor_name} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Sensor":
        current_info = self.get_info()
        updated_info = {k: v for k, v in current_info.items() if k not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info("API", f"Removed information from {self.sensor_name} in the database")
        return self
    
    @classmethod
    def search(
        cls,
        experiment_name: str = None,
        sensor_platform_name: str = None,
        sensor_type: GEMINISensorType = None,
        sensor_data_type: GEMINIDataType = None,
        sensor_data_format: GEMINIDataFormat = None,
        **search_parameters: Any
    ) -> List["Sensor"]:
        db_sensor_platform = SensorPlatformModel.get_by_parameters(sensor_platform_name=sensor_platform_name)
        db_sensors = ExperimentSensorsViewModel.search(
            experiment_name=experiment_name,
            sensor_platform_id=db_sensor_platform.id if db_sensor_platform else None,
            sensor_type_id=sensor_type.value if sensor_type else None,
            sensor_data_type_id=sensor_data_type.value if sensor_data_type else None,
            sensor_data_format_id=sensor_data_format.value if sensor_data_format else None,
            **search_parameters
        )
        db_sensors = [cls.model_validate(db_sensor) for db_sensor in db_sensors]
        logger_service.info("API", f"Retrieved {len(db_sensors)} sensors from the database")
        return db_sensors if db_sensors else None    
    
    
    def get_platform(self) -> SensorPlatform:
        self.refresh()
        logger_service.info("API", f"Retrieved platform for {self.sensor_name} from the database")
        return self.sensor_platform
    
    def set_platform(self, sensor_platform_name: str) -> SensorPlatform:
        db_sensor_platform = SensorPlatformModel.get_by_parameters(sensor_platform_name=sensor_platform_name)
        self.update(sensor_platform_id=db_sensor_platform.id)
        logger_service.info("API", f"Set platform for {self.sensor_name} to {sensor_platform_name}")
        return self.sensor_platform
    
    def get_datasets(self) -> List[Dataset]:
        self.refresh()
        logger_service.info("API", f"Retrieved datasets for {self.sensor_name} from the database")
        return self.datasets
    
    # Todo: Data Handling
    def add_record(
            self,
            sensor_data: dict,
            timestamp: datetime = None,
            collection_date: date = None,
            dataset_name: str = 'Default',
            experiment_name: str = 'Default',
            season_name: str = '2023',
            site_name: str = 'Default',
            plot_number: int = -1,
            plot_row_number: int = -1,
            plot_column_number: int = -1,
            record_info: dict = {}
    ) -> bool:

        if timestamp is None:
            timestamp = datetime.now()

        collection_date = timestamp.date() if collection_date is None else collection_date

        if dataset_name is None:
            dataset_name = f"{self.sensor_name}_{collection_date}"

        info = {
            "experiment_name": experiment_name if experiment_name else None,
            "season_name": season_name if season_name else None,
            "site_name": site_name if site_name else None,
            "plot_number": plot_number if plot_number else None,
            "plot_row_number": plot_row_number if plot_row_number else None,
            "plot_column_number": plot_column_number if plot_column_number else None,
        }

        if record_info:
            info.update(record_info)

        record = SensorRecord.create(
            sensor_name=self.sensor_name,
            timestamp=timestamp,
            collection_date=collection_date,
            sensor_data=sensor_data,
            record_info=info,
            dataset_name=dataset_name
        )

        success = SensorRecord.add([record])
        logger_service.info("API", f"Added record to {self.sensor_name}") if success else logger_service.error("API", f"Failed to add record to {self.sensor_name}")
        return success


    def add_records(
        self,
        sensor_data: List[dict],
        timestamps: List[datetime] = None,
        collection_date: date = None,
        dataset_name: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        plot_numbers: List[int] = None,
        plot_row_numbers: List[int] = None,
        plot_column_numbers: List[int] = None,
        record_info: List[dict] = None
    ) -> bool:
        
        if timestamps is None:
            timestamps = [datetime.now() for _ in range(len(sensor_data))]

        if len(sensor_data) != len(timestamps):
            raise ValueError("Sensor data and timestamps must have the same length")
        
        
        collection_date = timestamps[0].date() if collection_date is None else collection_date

        if dataset_name is None:
            dataset_name = f"{self.sensor_name}_{collection_date}"

        
        db_sensor = SensorModel.get_by_parameters(sensor_name=self.sensor_name)
        db_dataset = DatasetModel.get_or_create(dataset_name=dataset_name)
        if db_dataset not in db_sensor.datasets:
            db_sensor.datasets.append(db_dataset)
            db_sensor.save()

        records = []

        for i in track(range(len(sensor_data)), description="Preparing records"):

            info = {
                "experiment_name": experiment_name if experiment_name else None,
                "season_name": season_name if season_name else None,
                "site_name": site_name if site_name else None,
                "plot_number": plot_numbers[i] if plot_numbers else None,
                "plot_row_number": plot_row_numbers[i] if plot_row_numbers else None,
                "plot_column_number": plot_column_numbers[i] if plot_column_numbers else None,
            }

            if record_info and record_info[i]:
                info.update(record_info[i])
        
            record = SensorRecord.create(
                sensor_name=self.sensor_name,
                timestamp=timestamps[i],
                collection_date=collection_date,
                sensor_data=sensor_data[i],
                record_info=info,
                dataset_name=dataset_name
            )

            records.append(record)

        logger_service.info("API", f"Adding records to {self.sensor_name}")
        success = SensorRecord.add(records)
        logger_service.info("API", f"Added records to {self.sensor_name}") if success else logger_service.error("API", f"Failed to add records to {self.sensor_name}")
        return success

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

        record_info = record_info if record_info else {}
        record_info.update({
            "experiment_name": experiment_name,
            "season_name": season_name,
            "site_name": site_name,
            "plot_number": plot_number,
            "plot_row_number": plot_row_number,
            "plot_column_number": plot_column_number
        })

        # Remove None values from record_info
        record_info = {k: v for k, v in record_info.items() if v is not None}

        return SensorRecord.search(
            sensor_name=self.sensor_name,
            collection_date=collection_date,
            record_info = record_info
        )

       

