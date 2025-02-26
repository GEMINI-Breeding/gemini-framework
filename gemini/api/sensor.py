from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.dataset import Dataset, GEMINIDatasetType
from gemini.api.enums import GEMINISensorType, GEMINIDataType, GEMINIDataFormat
from gemini.api.sensor_record import SensorRecord
from gemini.db.models.sensors import SensorModel
from gemini.db.models.sensor_types import SensorTypeModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.views.experiment_views import ExperimentSensorsViewModel
from gemini.db.models.associations import ExperimentSensorModel, SensorPlatformSensorModel, SensorDatasetModel
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
                db_sensor_platform = SensorTypeModel.get_by_parameters(sensor_platform_name=sensor_platform_name)
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
        sensor_type: GEMINISensorType = None,
        sensor_data_type: GEMINIDataType = None,
        sensor_data_format: GEMINIDataFormat = None,
        sensor_info: dict = None
    ) -> "Sensor":
        try:
            if not any([sensor_type, sensor_data_type, sensor_data_format, sensor_info]):
                raise Exception("At least one update parameter must be provided.")

            current_id = self.id
            sensor = SensorModel.get(current_id)
            sensor = SensorModel.update(
                sensor,
                sensor_type=sensor_type,
                sensor_data_type=sensor_data_type,
                sensor_data_format=sensor_data_format,
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
            datasets = sensor.datasets
            datasets = [Dataset.model_validate(dataset) for dataset in datasets]
            return datasets
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

    # def add_record(
    #     self,
    #     record: SensorRecord
    # ) -> bool:
    #     try:
    #         if record.timestamp is None:
    #             record.timestamp = datetime.now()
    #         if record.collection_date is None:
    #             record.collection_date = record.timestamp.date()
    #         if record.dataset_name is None:
    #             record.dataset_name = f"{self.sensor_name} Dataset"
    #         if record.sensor_name is None:
    #             record.sensor_name = self.sensor_name
    #         if record.record_info is None:
    #             record.record_info = {}

    #         record.sensor_id = self.id
    #         success = SensorRecord.add([record])
    #         return success
    #     except Exception as e:
    #         return False
        

    # def add_records(
    #     self,
    #     records: List[SensorRecord]
    # ) -> bool:
    #     try:
    #         for record in records:
    #             if record.timestamp is None:
    #                 record.timestamp = datetime.now()
    #             if record.collection_date is None:
    #                 record.collection_date = record.timestamp.date()
    #             if record.dataset_name is None:
    #                 record.dataset_name = f"{self.sensor_name} Dataset"
    #             if record.sensor_name is None:
    #                 record.sensor_name = self.sensor_name
    #             if record.record_info is None:
    #                 record.record_info = {}

    #             record.sensor_id = self.id
    #         success = SensorRecord.add(records)
    #         return success
    #     except Exception as e:
    #         return False
        

    # def get_records(
    #         self,
    #         collection_date: date = None,
    #         experiment_name: str = None,
    #         season_name: str = None,
    #         site_name: str = None,
    #         plot_number: int = None,
    #         plot_row_number: int = None,
    #         plot_column_number: int = None,
    #         record_info: dict = None
    # ) -> List[SensorRecord]:
    #     try:
    #         record_info = record_info if record_info else {}
    #         record_info = {k: v for k, v in record_info.items() if v is not None}

    #         records = SensorRecord.search(
    #             sensor_id=self.id,
    #             collection_date=collection_date,
    #             experiment_name=experiment_name,
    #             season_name=season_name,
    #             site_name=site_name,
    #             plot_number=plot_number,
    #             plot_row_number=plot_row_number,
    #             plot_column_number=plot_column_number,
    #             record_info=record_info
    #         )
    #         return records
    #     except Exception as e:
    #         raise e
