from typing import Optional, List, Any, Union, TYPE_CHECKING
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, ID
from gemini.api.sensor_type import SensorType
from gemini.api.data_type import DataType
from gemini.api.data_format import DataFormat
from gemini.api.dataset import Dataset
from gemini.api.sensor_record import SensorRecord
from gemini.server.database.models import (
    SensorModel,
    ExperimentModel,
    SensorPlatformModel,
    DatasetModel,
)
from gemini.server.database.models import ExperimentSensorsViewModel
from gemini.api.enums import GEMINIDataFormat, GEMINIDataType, GEMINISensorType

from uuid import UUID
from datetime import date, datetime
from rich.progress import track


class Sensor(APIBase):

    db_model = SensorModel

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("sensor_id", "id"))
    sensor_name: str
    sensor_info: Optional[dict] = None
    sensor_type_id: Optional[int] = None
    sensor_data_type_id: Optional[int] = None
    sensor_data_format_id: Optional[int] = None

    sensor_type: Optional[SensorType] = None
    data_type: Optional[DataType] = None
    data_format: Optional[DataFormat] = None
    datasets: Optional[List[Dataset]] = None

    @classmethod
    def create(
        cls,
        sensor_name: str = "Default",
        sensor_info: dict = {},
        sensor_platform_name: str = "Default",
        sensor_type: GEMINISensorType = GEMINIDataFormat.Default,
        sensor_data_type: GEMINIDataType = GEMINIDataType.Default,
        sensor_data_format: GEMINIDataFormat = GEMINIDataFormat.Default,
        experiment_name: str = "Default",
    ):

        db_experiment = ExperimentModel.get_by_parameters(
            experiment_name=experiment_name
        )
        db_sensor_platform = SensorPlatformModel.get_by_parameters(
            sensor_platform_name=sensor_platform_name
        )

        db_instance = cls.db_model.get_or_create(
            sensor_name=sensor_name,
            sensor_info=sensor_info,
            sensor_type_id=sensor_type.value,
            sensor_data_type_id=sensor_data_type.value,
            sensor_data_format_id=sensor_data_format.value,
        )

        if db_experiment and db_instance not in db_experiment.sensors:
            db_experiment.sensors.append(db_instance)
            db_experiment.save()

        if db_sensor_platform and db_instance not in db_sensor_platform.sensors:
            db_sensor_platform.sensors.append(db_instance)
            db_sensor_platform.save()

        instance = cls.model_validate(db_instance)
        return instance

    @classmethod
    def get(cls, sensor_name: str) -> "Sensor":
        db_instance = cls.db_model.get_by_parameters(sensor_name=sensor_name)
        return cls.model_validate(db_instance) if db_instance else None

    @classmethod
    def get_by_experiment(cls, experiment_name: str) -> List["Sensor"]:
        db_experiment = ExperimentModel.get_by_parameters(
            experiment_name=experiment_name
        )
        db_sensors = db_experiment.sensors
        return (
            [cls.model_validate(db_sensor) for db_sensor in db_sensors]
            if db_sensors
            else None
        )

    @classmethod
    def get_by_type(cls, sensor_type: GEMINISensorType) -> List["Sensor"]:
        db_sensors = SensorModel.search(sensor_type_id=sensor_type.value)
        return (
            [cls.model_validate(db_sensor) for db_sensor in db_sensors]
            if db_sensors
            else None
        )

    def get_by_platform(cls, sensor_platform_name: str) -> List["Sensor"]:
        db_sensor_platform = SensorPlatformModel.get_by_parameters(
            sensor_platform_name=sensor_platform_name
        )
        db_sensors = db_sensor_platform.sensors
        return (
            [cls.model_validate(db_sensor) for db_sensor in db_sensors]
            if db_sensors
            else None
        )

    def get_info(self) -> dict:
        self.refresh()
        return self.sensor_info

    def set_info(self, sensor_info: Optional[dict] = None) -> "Sensor":
        self.update(sensor_info=sensor_info)
        return self

    def add_info(self, sensor_info: Optional[dict] = None) -> "Sensor":
        current_info = self.get_info()
        updated_info = {**current_info, **sensor_info}
        self.set_info(updated_info)
        return self

    def remove_info(self, keys_to_remove: List[str]) -> "Sensor":
        current_info = self.get_info()
        updated_info = {
            k: v for k, v in current_info.items() if k not in keys_to_remove
        }
        self.set_info(updated_info)
        return self

    @classmethod
    def search(
        cls,
        experiment_name: str = None,
        sensor_type: GEMINISensorType = None,
        sensor_data_type: GEMINIDataType = None,
        sensor_data_format: GEMINIDataFormat = None,
        **search_parameters: Any,
    ) -> List["Sensor"]:

        db_sensors = ExperimentSensorsViewModel.search(
            experiment_name=experiment_name,
            sensor_type_id=sensor_type.value if sensor_type else None,
            sensor_data_type_id=sensor_data_type.value if sensor_data_type else None,
            sensor_data_format_id=(
                sensor_data_format.value if sensor_data_format else None
            ),
            **search_parameters,
        )
        db_sensors = [cls.model_validate(db_sensor) for db_sensor in db_sensors]
        return db_sensors if db_sensors else None

    def get_datasets(self) -> List[Dataset]:
        self.refresh()
        return self.datasets

    # Todo: Data Handling
    def add_record(
        self,
        sensor_data: dict,
        timestamp: datetime = None,
        collection_date: date = None,
        dataset_name: str = None,
        experiment_name: str = "Default",
        season_name: str = "2023",
        site_name: str = "Default",
        plot_number: int = -1,
        plot_row_number: int = -1,
        plot_column_number: int = -1,
        record_info: dict = {},
    ) -> SensorRecord:

        if timestamp is None:
            timestamp = datetime.now()

        collection_date = (
            timestamp.date() if collection_date is None else collection_date
        )

        if dataset_name is None:
            dataset_name = f"{self.sensor_name}_{collection_date}"

        db_sensor = SensorModel.get_by_parameters(sensor_name=self.sensor_name)
        db_dataset = DatasetModel.get_or_create(dataset_name=dataset_name)
        if db_dataset not in db_sensor.datasets:
            db_sensor.datasets.append(db_dataset)
            db_sensor.save()

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
            dataset_name=dataset_name,
        )
        SensorRecord.add([record])
        return record
        # if len(records) == 0 or not records:
        #     return None
        # return records[0]

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
        record_info: List[dict] = None,
    ) -> List[SensorRecord]:

        if timestamps is None:
            timestamps = [datetime.now() for _ in range(len(sensor_data))]

        if len(sensor_data) != len(timestamps):
            raise ValueError("Sensor data and timestamps must have the same length")

        collection_date = (
            timestamps[0].date() if collection_date is None else collection_date
        )

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
                "plot_column_number": (
                    plot_column_numbers[i] if plot_column_numbers else None
                ),
            }

            info = {k: v for k, v in info.items() if v is not None}

            if record_info and record_info[i]:
                info.update(record_info[i])

            record = SensorRecord.create(
                sensor_name=self.sensor_name,
                timestamp=timestamps[i],
                collection_date=collection_date,
                sensor_data=sensor_data[i],
                record_info=info,
                dataset_name=dataset_name,
            )

            records.append(record)

        SensorRecord.add(records)
        return list(records)

    def get_records(
        self,
        collection_date: date = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
        record_info: dict = None,
    ) -> List[SensorRecord]:

        record_info = record_info if record_info else {}
        record_info.update(
            {
                "experiment_name": experiment_name,
                "season_name": season_name,
                "site_name": site_name,
                "plot_number": plot_number,
                "plot_row_number": plot_row_number,
                "plot_column_number": plot_column_number,
            }
        )

        # Remove None values from record_info
        record_info = {k: v for k, v in record_info.items() if v is not None}

        return SensorRecord.search(
            sensor_name=self.sensor_name,
            collection_date=collection_date,
            record_info=record_info,
        )
