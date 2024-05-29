from typing import Optional, List, Any, Union
from gemini.api.base import APIBase
from gemini.api.sensor_type import SensorType
from gemini.api.data_type import DataType
from gemini.api.data_format import DataFormat
from gemini.api.sensor_platform import SensorPlatform
from gemini.api.dataset import Dataset
from gemini.api.sensor_record import SensorRecord
from gemini.models import SensorModel, ExperimentModel, SensorPlatformModel, DatasetModel
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
        sensor_name: str,
        sensor_info: dict = None,
        sensor_platform_name: str = None,
        sensor_type: GEMINISensorType = GEMINIDataFormat.Default,
        sensor_data_type: GEMINIDataType = GEMINIDataType.Default,
        sensor_data_format: GEMINIDataFormat = GEMINIDataFormat.Default,
        experiment_name: str = None
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
        return cls.model_validate(db_instance)
    
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
    
    def add_dataset(
            self,
            dataset_name: str,
            dataset_info: dict = None,
            is_derived: bool = False,
            collection_date: Optional[date] = None,
            dataset_type: GEMINIDataType = GEMINIDataType.Default
        ) -> Dataset:

        if not collection_date:
            collection_date = datetime.now().date()

        if not dataset_name:
            dataset_name = f"{self.sensor_name}_{collection_date}"

        db_sensor = SensorModel.get_by_parameters(sensor_name=self.sensor_name)

        created_dataset = DatasetModel.get_or_create(
            dataset_name=dataset_name,
            dataset_info=dataset_info,
            is_derived=is_derived,
            collection_date=collection_date,
            dataset_type_id=dataset_type.value
        )

        if db_sensor and created_dataset not in db_sensor.datasets:
            db_sensor.datasets.append(created_dataset)
            db_sensor.save()

        logger_service.info("API", f"Added dataset {dataset_name} to {self.sensor_name}")
        return Dataset.model_validate(created_dataset)
    
    # Todo: Data Handling
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
        plot_column_numbers: List[int] = None
    ) -> List[Any]:
        
        if timestamps is None:
            timestamps = [datetime.now() for _ in range(len(sensor_data))]

        if len(sensor_data) != len(timestamps):
            raise ValueError("Sensor data and timestamps must have the same length")
        
        
        collection_date = timestamps[0].date() if collection_date is None else collection_date

        if dataset_name is None:
            dataset_name = f"{self.sensor_name}_{collection_date}"

        records = []

        for i in track(range(len(sensor_data)), description="Preparing records"):

            record_info = {
                "experiment_name": experiment_name if experiment_name else None,
                "season_name": season_name if season_name else None,
                "site_name": site_name if site_name else None,
                "plot_number": plot_numbers[i] if plot_numbers else None,
                "plot_row_number": plot_row_numbers[i] if plot_row_numbers else None,
                "plot_column_number": plot_column_numbers[i] if plot_column_numbers else None
            }

        
            record = SensorRecord.create(
                sensor_name=self.sensor_name,
                timestamp=timestamps[i],
                collection_date=collection_date,
                sensor_data=sensor_data[i],
                record_info=record_info,
                dataset_name=dataset_name
            )

            records.append(record)

        logger_service.info("API", f"Adding records to {self.sensor_name}")
        SensorRecord.add(records)
        logger_service.info("API", f"Added records to {self.sensor_name}")
        return records
    

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

        records = SensorRecord.search(
            sensor_name=self.sensor_name,
            collection_date=collection_date,
            record_info = record_info
        )

        logger_service.info("API", f"Retrieved records for {self.sensor_name}")
        return records



# from gemini.api.base import APIBase
# from gemini.api.sensor_record import SensorRecord
# from gemini.api.enums import (
#     GEMINIDataFormat,
#     GEMINIDataType,
#     GEMINISensorType,
#     GEMINIDatasetType,
# )
# from gemini.models import (
#     SensorModel,
#     SensorTypeModel,
#     DataTypeModel,
#     DataFormatModel,
#     ExperimentModel,
#     SensorPlatformModel,
#     SensorDatasetModel,
#     DatasetModel,
# )
# from gemini.logger import logger_service

# from typing import Optional, List, Any
# import pandas as pd
# from datetime import datetime


# class Sensor(APIBase):

#     db_model = SensorModel

#     sensor_name: str
#     sensor_info: Optional[dict] = None

#     sensor_type_id: Optional[int] = None
#     sensor_data_type_id: Optional[int] = None
#     sensor_data_format_id: Optional[int] = None

#     sensor_type: Optional[dict] = None
#     data_type: Optional[dict] = None
#     data_format: Optional[dict] = None
#     platform: Optional[dict] = None
#     experiments: Optional[List[dict]] = None
#     datasets: Optional[List[dict]] = None

#     @classmethod
#     def create(
#         cls,
#         sensor_name: str,
#         sensor_info: dict = None,
#         sensor_type: GEMINISensorType = None,
#         sensor_data_type: GEMINIDataType = None,
#         sensor_data_format: GEMINIDataFormat = None,
#         experiment_name: str = None,
#         sensor_platform_name: str = None,
#     ):
#         """
#         Create a new sensor

#         Args:
#         sensor_name (str): The name of the sensor
#         sensor_info (dict, optional): Additional information about the sensor. Defaults to None.
#         sensor_type (GEMINISensorType, optional): The type of the sensor. Defaults to None.
#         sensor_data_type (GEMINIDataType, optional): The data type of the sensor. Defaults to None.
#         sensor_data_format (GEMINIDataFormat, optional): The data format of the sensor. Defaults to None.
#         experiment_name (str, optional): The name of the experiment to add. Defaults to None.
#         sensor_platform_name (str, optional): The name of the platform. Defaults to None.

#         Returns:
#         Sensor: The created sensor
#         """

#         experiment = ExperimentModel.get_by_parameter(
#             "experiment_name", experiment_name
#         )
#         sensor_platform = SensorPlatformModel.get_by_parameter(
#             "sensor_platform_name", sensor_platform_name
#         )

#         new_instance = cls.db_model.get_or_create(
#             sensor_name=sensor_name,
#             sensor_info=sensor_info,
#             sensor_type_id=sensor_type.value if sensor_type is not None else None,
#             sensor_data_type_id=(
#                 sensor_data_type.value if sensor_data_type is not None else None
#             ),
#             sensor_data_format_id=(
#                 sensor_data_format.value if sensor_data_format is not None else None
#             ),
#             sensor_platform_id=(
#                 sensor_platform.id if sensor_platform is not None else None
#             ),
#         )

#         if experiment is not None and experiment not in new_instance.experiments:
#             new_instance.experiments.append(experiment)
#             new_instance.save()

#         logger_service.info(
#             "API",
#             f"Created a new sensor with name {new_instance.sensor_name} in the database",
#         )
#         new_instance = cls.model_validate(new_instance)
#         return new_instance

#     @classmethod
#     def get_by_name(cls, sensor_name: str) -> "Sensor":
#         """
#         Get a sensor by name

#         Args:
#         sensor_name (str): The name of the sensor

#         Returns:
#         Sensor: The sensor with the given name
#         """
#         sensor = SensorModel.get_by_parameter("sensor_name", sensor_name)
#         sensor = cls.model_validate(sensor)
#         return sensor

#     @classmethod
#     def get_by_type(cls, sensor_type: GEMINISensorType) -> List["Sensor"]:
#         """
#         Get all the sensors of a given type

#         Args:
#         sensor_type (GEMINISensorType): The type of the sensor

#         Returns:
#         List[Sensor]: A list of all the sensors of the given type
#         """
#         sensors = SensorModel.search(sensor_type_id=sensor_type.value)
#         sensors = [cls.model_validate(sensor) for sensor in sensors]
#         return sensors

#     def get_info(self) -> dict:
#         """
#         Get the information about a sensor

#         Returns:
#         dict: The information about the sensor
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved information about {self.sensor_name} from the database",
#         )
#         return self.sensor_info

#     def set_info(self, sensor_info: Optional[dict] = None) -> "Sensor":
#         """
#         Set the information about a sensor

#         Args:
#         sensor_info (Optional[dict], optional): The information to set. Defaults to None.

#         Returns:
#         Sensor: The sensor with the updated information
#         """
#         self.update(sensor_info=sensor_info)
#         logger_service.info(
#             "API",
#             f"Updated information about {self.sensor_name} in the database",
#         )
#         return self

#     def add_info(self, sensor_info: Optional[dict] = None) -> "Sensor":
#         """
#         Add information to a sensor

#         Args:
#         sensor_info (Optional[dict], optional): The information to add. Defaults to None.

#         Returns:
#         Sensor: The sensor with the added information
#         """
#         current_info = self.get_info()
#         updated_info = {**current_info, **sensor_info}
#         self.set_info(updated_info)
#         logger_service.info(
#             "API",
#             f"Added information to {self.sensor_name} in the database",
#         )
#         return self

#     def remove_info(self, keys_to_remove: List[str]) -> "Sensor":
#         """
#         Remove information from a sensor

#         Args:
#         keys_to_remove (List[str]): The keys to remove

#         Returns:
#         Sensor: The sensor with the removed information
#         """
#         current_info = self.get_info()
#         for key in keys_to_remove:
#             current_info.pop(key, None)
#         self.set_info(current_info)
#         logger_service.info(
#             "API",
#             f"Removed information from {self.sensor_name} in the database",
#         )
#         return self

#     def get_platform(self) -> dict:
#         """
#         Get the platform of a sensor

#         Returns:
#         Any: The platform of the sensor
#         """
#         self.refresh()
#         platform = self.platform
#         logger_service.info(
#             "API",
#             f"Retrieved platform for {self.sensor_name} from the database",
#         )
#         return platform

#     def set_platform(self, sensor_platform_name: str) -> "Sensor":
#         """
#         Set the platform for a sensor

#         Args:
#         sensor_platform_name (str): The name of the platform

#         Returns:
#         Sensor: The sensor with the updated platform
#         """
#         sensor_platform = SensorPlatformModel.get_by_parameter(
#             "sensor_platform_name", sensor_platform_name
#         )
#         self.update(sensor_platform_id=sensor_platform.id)
#         logger_service.info(
#             "API",
#             f"Set platform for {self.sensor_name} to {sensor_platform_name}",
#         )
#         return self

#     def get_experiments(self) -> List[dict]:
#         """
#         Get the experiments associated with a sensor

#         Returns:
#         List[Any]: The experiments associated with the sensor
#         """
#         self.refresh()
#         experiments = self.experiments
#         logger_service.info(
#             "API",
#             f"Retrieved experiments associated with {self.sensor_name} from the database",
#         )
#         return experiments

#     def add_experiment(self, experiment_name: str) -> "Sensor":
#         """
#         Add an experiment to a sensor

#         Args:
#         experiment_name (str): The name of the experiment to add

#         Returns:
#         Sensor: The sensor with the added experiment
#         """
#         experiment = ExperimentModel.get_by_parameter(
#             "experiment_name", experiment_name
#         )
#         if experiment is None:
#             raise ValueError(f"Experiment {experiment_name} not found")
#         if experiment not in self.experiments:
#             self.experiments.append(experiment)
#             self.save()
#         logger_service.info(
#             "API",
#             f"Added experiment {experiment_name} to {self.sensor_name}",
#         )
#         return self

#     def get_datasets(self) -> List[dict]:
#         """
#         Get the datasets associated with a sensor

#         Returns:
#         List[dict]: The datasets associated with the sensor
#         """
#         self.refresh()
#         datasets = self.datasets
#         logger_service.info(
#             "API",
#             f"Retrieved datasets associated with {self.sensor_name} from the database",
#         )
#         return datasets

#     def add_dataset(self, dataset_name: str) -> "Sensor":
#         pass

#     def get_type(self) -> dict:
#         """
#         Get the type of a sensor

#         Returns:
#         dict: The type of the sensor
#         """
#         self.refresh()
#         sensor_type = self.sensor_type
#         logger_service.info(
#             "API",
#             f"Retrieved type for {self.sensor_name} from the database",
#         )
#         return sensor_type

#     def set_type(self, sensor_type: GEMINISensorType) -> "Sensor":
#         pass

#     def get_data_type(self) -> dict:
#         """
#         Get the data type of a sensor

#         Returns:
#         dict: The data type of the sensor
#         """
#         self.refresh()
#         data_type = self.data_type
#         logger_service.info(
#             "API",
#             f"Retrieved data type for {self.sensor_name} from the database",
#         )
#         return data_type

#     def set_data_type(self, sensor_data_type: GEMINIDataType) -> "Sensor":
#         pass

#     def get_data_format(self) -> dict:
#         """
#         Get the data format of a sensor

#         Returns:
#         dict: The data format of the sensor
#         """
#         self.refresh()
#         data_format = self.data_format
#         logger_service.info(
#             "API",
#             f"Retrieved data format for {self.sensor_name} from the database",
#         )
#         return data_format

#     def set_data_format(self, sensor_data_format: GEMINIDataFormat) -> "Sensor":
#         pass

#     # Todo: Sensor Data Handling
#     def get_records(
#         self,
#         collection_date: datetime = None,
#         experiment: str = None,
#         season: str = None,
#         site: str = None,
#         plot_number: int = None,
#         plot_row_number: int = None,
#         plot_column_number: int = None,
#         record_info: dict = None,
#         as_dataframe: bool = False,
#     ) -> List[SensorRecord]:
#         """
#         Get the records generated by a sensor

#         Args:
#         collection_date (datetime, optional): The collection date of the records. Defaults to None.
#         experiment (str, optional): The experiment of the records. Defaults to None.
#         season (str, optional): The season of the records. Defaults to None.
#         site (str, optional): The site of the records. Defaults to None.
#         plot_number (int, optional): The plot number of the records. Defaults to None.
#         plot_row_number (int, optional): The plot row number of the records. Defaults to None.
#         plot_column_number (int, optional): The plot column number of the records. Defaults to None.
#         record_info (dict, optional): The information about the records. Defaults to None.
#         as_dataframe (bool, optional): Whether to return the records as a pandas DataFrame. Defaults to False.
#         """
#         self.refresh()
#         searched_records = SensorRecord.search(
#             collection_date=collection_date,
#             experiment_name=experiment,
#             season_name=season,
#             site_name=site,
#             sensor_name=self.sensor_name,
#             plot_number=plot_number,
#             plot_row_number=plot_row_number,
#             plot_column_number=plot_column_number,
#             record_info=record_info,
#         )
#         logger_service.info(
#             "API",
#             f"Retrieved records generated by {self.sensor_name} from the database",
#         )
#         if as_dataframe:
#             searched_records = pd.DataFrame(searched_records)
#         return searched_records

#     def add_record(
#         self,
#         timestamp: datetime,
#         sensor_data: dict,
#         collection_date: datetime = None,
#         record_info: dict = None,
#         experiment_name: str = None,
#         season_name: str = None,
#         site_name: str = None,
#         plot_number: int = None,
#         plot_row_number: int = None,
#         plot_column_number: int = None,
#     ):
#         """
#         Add a record generated by a sensor

#         Args:
#         timestamp (datetime): The timestamp of the record
#         collection_date (datetime): The collection date of the record
#         sensor_data (dict): The data of the record
#         record_info (dict, optional): The information about the record. Defaults to None.
#         experiment_name (str, optional): The name of the experiment. Defaults to None.
#         season_name (str, optional): The name of the season. Defaults to None.
#         site_name (str, optional): The name of the site. Defaults to None.
#         plot_number (int, optional): The plot number. Defaults to None.
#         plot_row_number (int, optional): The plot row number. Defaults to None.
#         plot_column_number (int, optional): The plot column number. Defaults to None.
#         """
#         new_record = SensorRecord.create(
#             sensor_name=self.sensor_name,
#             timestamp=timestamp,
#             collection_date=collection_date if collection_date else timestamp.date(),
#             sensor_data=sensor_data,
#             record_info=record_info,
#             experiment_name=experiment_name,
#             season_name=season_name,
#             site_name=site_name,
#             plot_number=plot_number,
#             plot_row_number=plot_row_number,
#             plot_column_number=plot_column_number,
#         )
#         logger_service.info(
#             "API",
#             f"Added record generated by {self.sensor_name} to the database",
#         )
#         return new_record

#     def add_records(
#         self,
#         sensor_data: List[dict],
#         timestamps: List[datetime] = None,
#         record_info: dict = None,
#         experiment_name: str = None,
#         season_name: str = None,
#         site_name: str = None,
#         plot_number: List[int] = None,
#         plot_row_number: List[int] = None,
#         plot_column_number: List[int] = None,
#     ):
#         """
#         Add multiple records generated by a sensor

#         Args:
#         timestamps (List[datetime]): The timestamps of the records
#         sensor_data (List[dict]): The data of the records
#         record_info (dict, optional): The information about the records. Defaults to None.
#         experiment_name (str, optional): The name of the experiment. Defaults to None.
#         season_name (str, optional): The name of the season. Defaults to None.
#         site_name (str, optional): The name of the site. Defaults to None.
#         plot_number (int, optional): The plot number. Defaults to None.
#         plot_row_number (int, optional): The plot row number. Defaults to None.
#         plot_column_number (int, optional): The plot column number. Defaults to None.
#         """

#         if timestamps is None:
#             timestamps = [datetime.now() for _ in range(len(sensor_data))]

#         if len(timestamps) != len(sensor_data):
#             raise ValueError("Timestamps and record data must have the same length")

#         records = SensorRecord.create_bulk(
#             timestamp=timestamps,
#             sensor_name=self.sensor_name,
#             collection_date=[timestamp.date() for timestamp in timestamps],
#             sensor_data=sensor_data,
#             record_info=record_info,
#             experiment_name=experiment_name,
#             season_name=season_name,
#             site_name=site_name,
#             plot_number=plot_number,
#             plot_row_number=plot_row_number,
#             plot_column_number=plot_column_number,
#         )

#         logger_service.info(
#             "API",
#             f"Added records generated by {self.sensor_name} to the database",
#         )

#         return records
