from typing import Optional, List, Generator
from uuid import UUID
import os, mimetypes
from tqdm import tqdm

from gemini.api.types import ID
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, FileHandlerMixin
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.columnar.dataset_records import DatasetRecordModel
from gemini.db.models.views.dataset_records_immv import DatasetRecordsIMMVModel
from gemini.db.models.views.validation_views import ValidDatasetCombinationsViewModel
from gemini.db.models.views.experiment_views import (
    ExperimentDatasetsViewModel,
    ExperimentSeasonsViewModel,
    ExperimentSitesViewModel
)

from gemini.db.models.experiments import ExperimentModel

from datetime import date, datetime

class DatasetRecord(APIBase, FileHandlerMixin):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "dataset_record_id"))

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id: Optional[ID] = None
    dataset_name: Optional[str] = None
    dataset_data: Optional[dict] = None
    experiment_name: Optional[str] = None
    experiment_id: Optional[ID] = None
    season_name: Optional[str] = None
    season_id: Optional[ID] = None
    site_name: Optional[str] = None
    site_id: Optional[ID] = None
    record_file: Optional[str] = None
    record_info: Optional[dict] = None

    def __str__(self):
        return f"DatasetRecord(id={self.id}, timestamp={self.timestamp}, dataset_name={self.dataset_name}, experiment_name={self.experiment_name}, season_name={self.season_name}, site_name={self.site_name})"
    
    def __repr__(self):
        return f"DatasetRecord(id={self.id}, timestamp={self.timestamp}, dataset_name={self.dataset_name}, experiment_name={self.experiment_name}, season_name={self.season_name}, site_name={self.site_name})"
    
    @classmethod
    def exists(
        cls,
        timestamp: datetime,
        dataset_name: str,
        experiment_name: str,
        season_name: str,
        site_name: str,
    ) -> bool:
        try:
            exists = DatasetRecordModel.exists(
                timestamp=timestamp,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            return exists
        except Exception as e:
            print(f"Error checking existence: {e}")
            return False
        
    @classmethod
    def create(
        cls,
        timestamp: datetime = datetime.now(),
        collection_date: date = None,
        dataset_name: str = None,
        dataset_data: dict = {},
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        record_file: str = None,
        record_info: dict = {},
        insert_on_create: bool = True
    ) -> Optional["DatasetRecord"]:
        try:
            if not any([experiment_name, site_name, season_name]):
                raise ValueError("At least one of experiment_name, site_name, or season_name is required.")
            if not dataset_name:
                raise ValueError("dataset_name is required.")
            if not timestamp:
                raise ValueError("timestamp is required.")
            if not collection_date:
                collection_date = timestamp.date()
            if not dataset_data and not record_file:
                raise ValueError("Either dataset_data or record_file is required.")
            dataset_record = DatasetRecord(
                timestamp=timestamp,
                collection_date=collection_date,
                dataset_name=dataset_name,
                dataset_data=dataset_data,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                record_file=record_file,
                record_info=record_info
            )
            if insert_on_create:
                insert_success, inserted_record_ids = cls.insert([dataset_record])
                if not insert_success:
                    print(f"Failed to insert DatasetRecord: {dataset_record}")
                    return None
                if not inserted_record_ids or len(inserted_record_ids) == 0:
                    print(f"No new DatasetRecord was inserted.")
                    return None
                inserted_record_id = inserted_record_ids[0]
                dataset_record = cls.get_by_id(inserted_record_id)
            return dataset_record
        except Exception as e:
            print(f"Error creating DatasetRecord: {e}")
            return None
    

    @classmethod
    def insert(cls, records: List["DatasetRecord"]) -> tuple[bool, List[str]]:
        try:
            if not records or len(records) == 0:
                print(f"No records provided to insert.")
                return False, []
            records = cls.verify_records(records)
            records = [cls.process_record(record) for record in tqdm(records, desc="Processing Records for Dataset: " + records[0].dataset_name)]
            records_to_insert = []
            for record in records:
                record_dict = record.model_dump()
                record_dict = {k: v for k, v in record_dict.items() if v is not None}
                records_to_insert.append(record_dict)
            print(f"Inserting {len(records_to_insert)} records.")
            inserted_record_ids = DatasetRecordModel.insert_bulk('dataset_records_unique', records_to_insert)
            print(f"Inserted {len(inserted_record_ids)} records.")
            return True, inserted_record_ids
        except Exception as e:
            print(f"Error inserting records: {e}")
            return False, []

    @classmethod
    def get(
        cls,
        timestamp: datetime,
        dataset_name: str,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
    ) -> Optional["DatasetRecord"]:
        try:
            if not timestamp:
                print(f"Timestamp is required to get the DatasetRecord.")
                return None
            if not dataset_name:
                print(f"Dataset name is required to get the DatasetRecord.")
                return None
            if not experiment_name and not season_name and not site_name:
                print(f"At least one of experiment_name, season_name, or site_name is required to get the DatasetRecord.")
                return None
            dataset_record = DatasetRecordsIMMVModel.get_by_parameters(
                timestamp=timestamp,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            if not dataset_record:
                print(f"DatasetRecord not found.")
                return None
            dataset_record = cls.model_validate(dataset_record)
            return dataset_record
        except Exception as e:
            print(f"Error getting DatasetRecord: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["DatasetRecord"]:
        try:
            db_instance = DatasetRecordModel.get(id)
            if not db_instance:
                print(f"DatasetRecord with id {id} not found.")
                return None
            record = cls.model_validate(db_instance)
            return record
        except Exception as e:
            print(f"Error getting DatasetRecord by id: {e}")
            return None
        
    @classmethod
    def get_all(cls, limit: int = 100) -> Optional[List["DatasetRecord"]]:
        try:
            records = DatasetRecordModel.all(limit=limit)
            if not records or len(records) == 0:
                print(f"No DatasetRecords found.")
                return None
            records = [cls.model_validate(record) for record in records]
            return records
        except Exception as e:
            print(f"Error getting all DatasetRecords: {e}")
            return None


    @classmethod
    def search(
        cls,
        dataset_name: str = None,
        dataset_data: dict = None,
        experiment_name: str = None,    
        season_name: str = None,
        site_name: str = None,
        collection_date: date = None,
        record_info: dict = None,
    ) -> Generator["DatasetRecord", None, None]:
        try:
            if not any([dataset_name, dataset_data, experiment_name, season_name, site_name, collection_date, record_info]):
                raise ValueError("At least one parameter must be provided.")
            records = DatasetRecordsIMMVModel.stream(
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                collection_date=collection_date,
                dataset_data=dataset_data,
                record_info=record_info
            )
            for record in records:
                record = cls.model_validate(record)
                yield record
        except Exception as e:
            print(f"Error searching DatasetRecords: {e}")
            yield None

    @classmethod
    def filter(
        cls,
        dataset_names: List[str] = None,
        start_timestamp: datetime = None,
        end_timestamp: datetime = None,
        experiment_names: List[str] = None,
        season_names: List[str] = None,
        site_names: List[str] = None
    ) -> Generator["DatasetRecord", None, None]:
        try:
            if not any([dataset_names, start_timestamp, end_timestamp, experiment_names, season_names, site_names]):
                raise ValueError("At least one parameter must be provided.")
            records = DatasetRecordModel.filter_records(
                dataset_names=dataset_names,
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
                experiment_names=experiment_names,
                season_names=season_names,
                site_names=site_names
            )
            for record in records:
                record = cls.model_validate(record)
                yield record
        except Exception as e:
            print(f"Error filtering DatasetRecords: {e}")
            yield None

    
    def update(
        self,
        dataset_data: dict = None,
        record_info: dict = None
    ) -> Optional["DatasetRecord"]:
        try:
            if not any([dataset_data, record_info]):
                print(f"At least one parameter must be provided to update the DatasetRecord.")
                return None
            current_id = self.id
            dataset_record = DatasetRecordModel.get(current_id)
            if not dataset_record:
                print(f"DatasetRecord with id {current_id} not found.")
                return None
            dataset_record = DatasetRecordModel.update(
                dataset_record,
                dataset_data=dataset_data,
                record_info=record_info
            )
            dataset_record = self.model_validate(dataset_record)
            self.refresh()
            return dataset_record
        except Exception as e:
            print(f"Error updating DatasetRecord: {e}")
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            dataset_record = DatasetRecordModel.get(current_id)
            if not dataset_record:
                print(f"DatasetRecord with id {current_id} not found.")
                return False
            DatasetRecordModel.delete(dataset_record)
            return True
        except Exception as e:
            print(f"Error deleting DatasetRecord: {e}")
            return False
        
    def refresh(self) -> Optional["DatasetRecord"]:
        try:
            db_instance = DatasetRecordModel.get(self.id)
            if not db_instance:
                print(f"DatasetRecord with id {self.id} not found.")
                return None
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing DatasetRecord: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            dataset_record = DatasetRecordModel.get(current_id)
            if not dataset_record:
                print(f"DatasetRecord with id {current_id} not found.")
                return None
            record_info = dataset_record.record_info
            if not record_info:
                print(f"No record info found for DatasetRecord with id {current_id}.")
                return None
            return record_info
        except Exception as e:
            print(f"Error getting record info: {e}")
            return None

    def set_info(self, record_info: dict) -> Optional["DatasetRecord"]:
        try:
            current_id = self.id
            dataset_record = DatasetRecordModel.get(current_id)
            if not dataset_record:
                print(f"DatasetRecord with id {current_id} not found.")
                return None
            dataset_record = DatasetRecordModel.update(
                dataset_record,
                record_info=record_info
            )
            dataset_record = self.model_validate(dataset_record)
            self.refresh()
            return dataset_record
        except Exception as e:
            print(f"Error setting record info: {e}")
            return None
    
    @classmethod
    def create_file_uri(cls, record: "DatasetRecord") -> Optional[str]:
        try:
            original_file_path = record.record_file
            if not original_file_path:
                print(f"record_file is required to create file URI.")
                return None
            if not os.path.exists(original_file_path):
                print(f"File {original_file_path} does not exist.")
                return None
            # Assuming the file is stored in a specific structure, we can create a file URI
            collection_date = record.collection_date.strftime("%Y-%m-%d")
            dataset_name = record.dataset_name
            experiment_name = record.experiment_name
            season_name = record.season_name
            site_name = record.site_name
            file_extension = os.path.splitext(original_file_path)[1]
            file_timestamp = str(int(record.timestamp.timestamp() * 1000))
            file_key = f"dataset_data/{experiment_name}/{dataset_name}/{collection_date}/{site_name}/{season_name}/{file_timestamp}{file_extension}"
            return file_key
        except Exception as e:
            print(f"Error creating file URI: {e}")
            return None


    @classmethod
    def process_record(cls, record: "DatasetRecord") -> "DatasetRecord":
        try:
            file = record.record_file
            if not file:
                return record
            file_key = cls.create_file_uri(record)
            if not file_key:
                print(f"Failed to create file URI for record: {record}")
                return record
            content_type, _ = mimetypes.guess_type(file)
            # Generate Metadata for upload
            file_metadata = {
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
            print(f"Error processing record: {e}")
            return record

            
   