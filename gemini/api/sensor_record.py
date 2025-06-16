from typing import Optional, List, Generator
import os, mimetypes
from tqdm import tqdm   
from uuid import UUID

from gemini.api.types import ID
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, FileHandlerMixin
from gemini.api.dataset import Dataset, GEMINIDatasetType
from gemini.api.plot import Plot
from gemini.db.models.sensors import SensorModel
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.columnar.sensor_records import SensorRecordModel
from gemini.db.models.views.validation_views import ValidSensorDatasetCombinationsViewModel
from gemini.db.models.views.sensor_records_immv import SensorRecordsIMMVModel
from gemini.db.models.views.plot_view import PlotViewModel
from gemini.db.models.views.dataset_views import SensorDatasetsViewModel
from gemini.db.models.views.experiment_views import (
    ExperimentSensorsViewModel,
    ExperimentDatasetsViewModel,
    ExperimentSitesViewModel,
    ExperimentSeasonsViewModel
)

from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.associations import (
    SensorDatasetModel,
    ExperimentDatasetModel,
    ExperimentSensorModel,
    ExperimentSiteModel,

)

from datetime import date, datetime

class SensorRecord(APIBase, FileHandlerMixin):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "sensor_record_id"))

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id: Optional[ID] = None
    dataset_name: Optional[str] = None
    sensor_id: Optional[ID] = None
    sensor_name: Optional[str] = None
    sensor_data: Optional[dict] = None
    experiment_id: Optional[ID] = None
    experiment_name : Optional[str] = None
    season_id: Optional[ID] = None
    season_name: Optional[str] = None
    site_id: Optional[ID] = None
    site_name: Optional[str] = None
    plot_id: Optional[ID] = None
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    record_file: Optional[str] = None
    record_info: Optional[dict] = None

    def __str__(self):
        return f"SensorRecord(id={self.id}, timestamp={self.timestamp}, sensor_name={self.sensor_name}, dataset_name={self.dataset_name}, experiment_name={self.experiment_name}, site_name={self.site_name}, season_name={self.season_name}, plot_number={self.plot_number})"
    
    def __repr__(self):
        return f"SensorRecord(id={self.id}, timestamp={self.timestamp}, sensor_name={self.sensor_name}, dataset_name={self.dataset_name}, experiment_name={self.experiment_name}, site_name={self.site_name}, season_name={self.season_name}, plot_number={self.plot_number})"
    
    @classmethod
    def exists(
        cls,
        timestamp: datetime,
        sensor_name: str,
        dataset_name: str,
        experiment_name: str,
        season_name: str,
        site_name: str,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None
    ) -> bool:
        try:
            exists = SensorRecordModel.exists(
                timestamp=timestamp,
                sensor_name=sensor_name,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number
            )
            return exists
        except Exception as e:
            print(f"Error checking existence of sensor record: {e}")
            return False
        
    @classmethod
    def create(
        cls,
        timestamp: datetime = datetime.now(),
        collection_date: date = None,
        dataset_name: str = None,
        sensor_name: str = None,
        sensor_data: dict = {},
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
        record_file: str = None,
        record_info: dict = {},
        insert_on_create: bool = True
    ) -> Optional["SensorRecord"]:
        try:
            if not any([experiment_name, season_name, site_name]):
                raise ValueError("At least one of experiment_name, season_name, or site_name must be provided.")
            if not sensor_name:
                raise ValueError("Sensor name is required.")
            if not dataset_name:
                raise ValueError("Dataset name is required.")
            if not all([plot_number, plot_row_number, plot_column_number]):
                raise ValueError("Plot number, plot row number, and plot column number are required if a plot is specified.")
            if not timestamp:
                timestamp = datetime.now()
            if not collection_date:
                collection_date = timestamp.date()
            if not sensor_data and not record_file:
                raise ValueError("Either sensor_data or record_file must be provided.")
            sensor_record = SensorRecord(
                timestamp=timestamp,
                collection_date=collection_date,
                dataset_name=dataset_name,
                sensor_name=sensor_name,
                sensor_data=sensor_data,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                record_file=record_file,
                record_info=record_info
            )
            if insert_on_create:
                insert_success, inserted_record_ids = cls.insert([sensor_record])
                if not insert_success:
                    print("Failed to insert SensorRecord.")
                    return None
                if not inserted_record_ids or len(inserted_record_ids) == 0:
                    print("No new SensorRecord was inserted.")
                    return None
                inserted_record_id = inserted_record_ids[0]
                sensor_record = cls.get_by_id(inserted_record_id)
            return sensor_record    
        except Exception as e:
            print(f"Error creating sensor record: {e}")
            return None
    
    @classmethod
    def insert(cls, records: List["SensorRecord"]) -> tuple[bool, List[str]]:
        try:
            if not records or len(records) == 0:
                raise ValueError("No records provided for insertion.")
                return False, []
            records = [cls.process_record(record) for record in tqdm(records, desc="Processing Records for Sensor: " + records[0].sensor_name)]
            records_to_insert = []
            for record in records:
                record_to_insert = record.model_dump()
                record_to_insert = {k: v for k, v in record_to_insert.items() if v is not None}
                records_to_insert.append(record_to_insert)
            print(f"Inserting {len(records_to_insert)} records.")
            inserted_record_ids = SensorRecordModel.insert_bulk('sensor_records_unique', records_to_insert)
            print(f"Inserted {len(inserted_record_ids)} records.")
            return True, inserted_record_ids
        except Exception as e:
            print(f"Error inserting records: {e}")
            return False, []
        
    @classmethod
    def get(
        cls,
        timestamp: datetime,
        sensor_name: str,
        dataset_name: str,
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None
    ) -> Optional["SensorRecord"]:
        try:
            if not timestamp:
                print("Timestamp is required to get a sensor record.")
                return None
            if not dataset_name:
                print("Dataset name is required to get a sensor record.")
                return None
            if not sensor_name:
                print("Sensor name is required to get a sensor record.")
                return None
            if not experiment_name and not site_name and not season_name:
                print("At least one of experiment_name, site_name, or season_name is required to get a sensor record.")
                return None
            if not all([plot_number, plot_row_number, plot_column_number]):
                print("Plot number, plot row number, and plot column number are required if a plot is specified.")
                return None
            sensor_record = SensorRecordsIMMVModel.get_by_parameters(
                timestamp=timestamp,
                sensor_name=sensor_name,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number
            )
            if not sensor_record:
                print("No sensor record found with the provided parameters.")
                return None
            sensor_record = cls.model_validate(sensor_record)
            return sensor_record
        except Exception as e:
            print(f"Error getting sensor record: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["SensorRecord"]:
        try:
            db_instance = SensorRecordModel.get(id)
            if not db_instance:
                print(f"No sensor record found with ID: {id}")
                return None
            record = cls.model_validate(db_instance)
            return record
        except Exception as e:
            print(f"Error getting sensor record by ID: {e}")
            return None
        
    @classmethod
    def get_all(cls, limit: int = 100) -> Optional[List["SensorRecord"]]:
        try:
            records = SensorRecordModel.all(limit=limit)
            if not records or len(records) == 0:
                print("No sensor records found.")
                return None
            records = [cls.model_validate(record) for record in records]
            return records
        except Exception as e:
            print(f"Error getting all sensor records: {e}")
            return None
        
    @classmethod
    def search(
        cls,
        sensor_name: str = None,
        sensor_data: dict = None,
        dataset_name: str = None,
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
        collection_date: date = None,
        record_info: dict = None
    ) -> Generator["SensorRecord", None, None]:
        try:
            if not any([sensor_name, dataset_name, experiment_name, site_name, season_name, plot_number, plot_row_number, plot_column_number]):
                print("At least one search parameter must be provided.")
                return
            records = SensorRecordsIMMVModel.stream(
                sensor_name=sensor_name,
                sensor_data=sensor_data,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                collection_date=collection_date,
                record_info=record_info
            )
            for record in records:
                record = cls.model_validate(record)
                yield record
        except Exception as e:
            print(f"Error searching sensor records: {e}")
            yield from []

    @classmethod
    def filter(
        cls,
        start_timestamp: datetime = None,
        end_timestamp: datetime = None,
        sensor_names: List[str] = None,
        dataset_names: List[str] = None,
        experiment_names: List[str] = None,
        site_names: List[str] = None,
        season_names: List[str] = None
    ) -> Generator["SensorRecord", None, None]:
        try:
            records = SensorRecordModel.filter_records(
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
                sensor_names=sensor_names,
                dataset_names=dataset_names,
                experiment_names=experiment_names,
                site_names=site_names,
                season_names=season_names
            )
            for record in records:
                record = cls.model_validate(record)
                yield record
        except Exception as e:
            print(f"Error filtering sensor records: {e}")
            yield from []
    

    def update(
        self,
        sensor_data: dict = None,
        record_info: dict = None
    ) -> Optional["SensorRecord"]:
        try:
            if not any([sensor_data, record_info]):
                print("At least one update parameter must be provided.")
                return None
            current_id = self.id
            sensor_record = SensorRecordModel.get(current_id)
            if not sensor_record:
                print(f"No sensor record found with ID: {current_id}")
                return None
            sensor_record = SensorRecordModel.update(
                sensor_record,
                sensor_data=sensor_data,
                record_info=record_info
            )
            sensor_record = self.model_validate(sensor_record)
            self.refresh()
            return sensor_record
        except Exception as e:
            print(f"Error updating sensor record: {e}")
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            sensor_record = SensorRecordModel.get(current_id)
            if not sensor_record:
                print(f"No sensor record found with ID: {current_id}")
                return False
            SensorRecordModel.delete(sensor_record)
            return True
        except Exception as e:
            print(f"Error deleting sensor record: {e}")
            return False
        
    def refresh(self) -> Optional["SensorRecord"]:
        try:
            db_instance = SensorRecordModel.get(self.id)
            if not db_instance:
                print(f"SensorRecord with id {self.id} not found.")
                return None
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing SensorRecord: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            sensor_record = SensorRecordModel.get(current_id)
            if not sensor_record:
                print(f"No sensor record found with ID: {current_id}")
                return None
            record_info = sensor_record.record_info
            if not record_info:
                print("No record info available for this sensor record.")
                return None
            return record_info
        except Exception as e:
            print(f"Error getting sensor record info: {e}")
            return None
            

    def set_info(self, record_info: dict) -> Optional["SensorRecord"]:
        try:
            current_id = self.id
            sensor_record = SensorRecordModel.get(current_id)
            if not sensor_record:
                print(f"No sensor record found with ID: {current_id}")
                return None
            SensorRecordModel.update(
                sensor_record,
                record_info=record_info
            )
            sensor_record = self.model_validate(sensor_record)
            self.refresh()
            return sensor_record
        except Exception as e:
            print(f"Error setting sensor record info: {e}")
            return None
    
    @classmethod
    def create_file_uri(cls, record: "SensorRecord") -> Optional[str]:
        try:
            original_file_path = record.record_file
            if not original_file_path:
                print(f"record_file is required to create file URI.")
                return None
            if not os.path.exists(original_file_path):
                print(f"File {original_file_path} does not exist.")
                return None
            collection_date = record.collection_date.strftime("%Y-%m-%d")
            sensor_name = record.sensor_name
            dataset_name = record.dataset_name
            experiment_name = record.experiment_name
            season_name = record.season_name
            site_name = record.site_name
            file_extension = os.path.splitext(original_file_path)[1]
            file_timestamp = str(int(record.timestamp.timestamp() * 1000))
            file_key = f"sensor_data/{experiment_name}/{sensor_name}/{dataset_name}/{collection_date}/{site_name}/{season_name}/{file_timestamp}{file_extension}"
            return file_key
        except Exception as e:
            print(f"Error creating file URI: {e}")
            return None


    @classmethod
    def process_record(cls, record: "SensorRecord") -> "SensorRecord":
        try:
            file = record.record_file
            if not file:
                print(f"record_file is required to process SensorRecord.")
                return record
            file_key = cls.create_file_uri(record)
            if not file_key:
                print(f"Failed to create file URI for SensorRecord: {record}")
                return record
            content_type, _ = mimetypes.guess_type(file)
            # Generate Metadata for upload
            file_metadata = {
                "Sensor-Name": record.sensor_name,
                "Dataset-Name": record.dataset_name,
                "Experiment-Name": record.experiment_name,
                "Site-Name": record.site_name,
                "Season-Name": record.season_name,
                "Collection-Date": record.collection_date.isoformat() if record.collection_date else None,
                "Timestamp": record.timestamp.isoformat() if record.timestamp else None,
            }
            cls.minio_storage_provider.upload_file(
                object_name=file_key,
                input_file_path=file,
                bucket_name="gemini",
                content_type=content_type,
                metadata=file_metadata
            )
            record.record_file = file_key
            return record
        except Exception as e:
            print(f"Error processing SensorRecord: {e}")
            return record