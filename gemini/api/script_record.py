from typing import Optional, List, Generator
import os, mimetypes
from uuid import UUID
from tqdm import tqdm

from gemini.api.types import ID
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, FileHandlerMixin
from gemini.api.dataset import Dataset, GEMINIDatasetType
from gemini.db.models.scripts import ScriptModel
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.columnar.script_records import ScriptRecordModel
from gemini.db.models.views.script_records_immv import ScriptRecordsIMMVModel
from gemini.db.models.views.dataset_views import ScriptDatasetsViewModel
from gemini.db.models.views.validation_views import ValidScriptDatasetCombinationsViewModel
from gemini.db.models.views.experiment_views import (
    ExperimentScriptsViewModel,
    ExperimentDatasetsViewModel,
    ExperimentSeasonsViewModel,
    ExperimentSitesViewModel
)

from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.associations import ScriptDatasetModel

from datetime import date, datetime

class ScriptRecord(APIBase, FileHandlerMixin):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "script_record_id"))

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id: Optional[ID] = None
    dataset_name: Optional[str] = None
    script_id: Optional[ID] = None
    script_name: Optional[str] = None
    script_data: Optional[dict] = None
    experiment_id: Optional[ID] = None
    experiment_name : Optional[str] = None
    season_id: Optional[ID] = None
    season_name: Optional[str] = None
    site_id: Optional[ID] = None
    site_name: Optional[str] = None
    record_file: Optional[str] = None
    record_info: Optional[dict] = None

    def __str__(self):
        return f"ScriptRecord(id={self.id}, timestamp={self.timestamp}, script_name={self.script_name}, dataset_name={self.dataset_name}, experiment_name={self.experiment_name}, site_name={self.site_name}, season_name={self.season_name})"
    
    def __repr__(self):
        return f"ScriptRecord(id={self.id}, timestamp={self.timestamp}, script_name={self.script_name}, dataset_name={self.dataset_name}, experiment_name={self.experiment_name}, site_name={self.site_name}, season_name={self.season_name})"
    
    @classmethod
    def exists(
        cls,
        timestamp: datetime,
        script_name: str,
        dataset_name: str,
        experiment_name: str,
        season_name: str,
        site_name: str
    ) -> bool:
        try:
            exists = ScriptRecordModel.exists(
                timestamp=timestamp,
                script_name=script_name,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            return exists
        except Exception as e:
            print(f"Error checking existence of ScriptRecord: {e}")
            raise e
        
    @classmethod
    def create(
        cls,
        timestamp: datetime = datetime.now(),
        collection_date: date = None,
        dataset_name: str = None,
        script_name: str = None,
        script_data: dict = {},
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        record_file: str = None,
        record_info: dict = {},
        insert_on_create: bool = True
    ) -> Optional["ScriptRecord"]:
        try:
            if not any([experiment_name, site_name, season_name]):
                raise ValueError("At least one of experiment_name, site_name, or season_name must be provided.")
            if not script_name:
                raise ValueError("Script name is required.")
            if not dataset_name:
                raise ValueError("Dataset name is required.")
            if not timestamp:
                raise ValueError("Timestamp is required.")
            if not collection_date:
                collection_date = timestamp.date()
            if not script_data and not record_file:
                raise ValueError("At least one of script_data or record_file must be provided.")
            script_record = ScriptRecord(
                timestamp=timestamp,
                collection_date=collection_date,
                dataset_name=dataset_name,
                script_name=script_name,
                script_data=script_data,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                record_file=record_file,
                record_info=record_info
            )
            if insert_on_create:
                insert_success, inserted_record_ids = cls.insert([script_record])
                if not insert_success:
                    print(f"Failed to insert ScriptRecord: {script_record}")
                    return None
                if not inserted_record_ids or len(inserted_record_ids) == 0:
                    print(f"No new ScriptRecord was inserted.")
                    return None
                inserted_record_id = inserted_record_ids[0]
                script_record = cls.get_by_id(inserted_record_id)
            return script_record
        except Exception as e:
            print(f"Error creating ScriptRecord: {e}")
            raise None
        
    @classmethod
    def insert(cls, records: List["ScriptRecord"]) -> tuple[bool, List[str]]:
        try:
            if not records or len(records) == 0:
                print(f"No records provided for insertion.")
                return False, []
            records = [cls.process_record(record) for record in tqdm(records, desc="Processing ScriptRecords")]
            records_to_insert = []
            for record in records:
                record_dict = record.model_dump()
                record_dict = {k: v for k, v in record_dict.items() if v is not None}
                records_to_insert.append(record_dict)
            print(f"Inserting {len(records_to_insert)} records.")
            inserted_record_ids = ScriptRecordModel.insert_bulk('script_records_unique', records_to_insert)
            print(f"Inserted {len(inserted_record_ids)} records.")
            return True, inserted_record_ids
        except Exception as e:
            print(f"Error inserting ScriptRecords: {e}")
            return False, []
        
    @classmethod
    def get(
        cls,
        timestamp: datetime,
        script_name: str,
        dataset_name: str,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None
    ) -> Optional["ScriptRecord"]:
        try:
            if not timestamp:
                print(f"Timestamp is required to get ScriptRecord.")
                return None
            if not dataset_name:
                print(f"Dataset name is required to get ScriptRecord.")
                return None
            if not script_name:
                print(f"Script name is required to get ScriptRecord.")
                return None
            if not experiment_name and not season_name and not site_name:
                print(f"At least one of experiment_name, season_name, or site_name is required to get ScriptRecord.")
                return None
            script_record = ScriptRecordsIMMVModel.get_by_parameters(
                timestamp=timestamp,
                script_name=script_name,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            if not script_record:
                print(f"No ScriptRecord found for the given parameters.")
                return None
            script_record = cls.model_validate(script_record)
            return script_record
        except Exception as e:
            print(f"Error getting ScriptRecord: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["ScriptRecord"]:
        try:
            db_instance = ScriptRecordModel.get(id)
            if not db_instance:
                print(f"No ScriptRecord found with ID: {id}")
                return None
            record = cls.model_validate(db_instance)
            return record
        except Exception as e:
            print(f"Error getting ScriptRecord by ID: {e}")
            return None
        
    @classmethod
    def get_all(cls, limit: int = 100) -> Optional[List["ScriptRecord"]]:
        try:
            records = ScriptRecordModel.all(limit=limit)
            if not records or len(records) == 0:
                print(f"No ScriptRecords found.")
                return None
            records = [cls.model_validate(record) for record in records]
            return records
        except Exception as e:
            print(f"Error getting all ScriptRecords: {e}")
            return None
        
    @classmethod
    def search(
        cls,
        script_name: str = None,
        script_data: dict = None,
        dataset_name: str = None,
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        collection_date: date = None,
        record_info: dict = None
    ) -> Generator["ScriptRecord", None, None]:
        try:
            if not any([script_name, dataset_name, experiment_name, site_name, season_name, collection_date, record_info]):
                print(f"At least one parameter must be provided for search.")
                return
            records = ScriptRecordsIMMVModel.stream(
                script_name=script_name,
                script_data=script_data,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                collection_date=collection_date,
                record_info=record_info
            )
            for record in records:
                record = cls.model_validate(record)
                yield record
        except Exception as e:
            print(f"Error searching ScriptRecords: {e}")
            yield None

    @classmethod
    def filter(
        cls,
        start_timestamp: datetime = None,
        end_timestamp: datetime = None,
        script_names: List[str] = None,
        dataset_names: List[str] = None,
        experiment_names: List[str] = None,
        season_names: List[str] = None,
        site_names: List[str] = None
    ) -> Generator["ScriptRecord", None, None]:
        try:
            if not any([start_timestamp, end_timestamp, script_names, dataset_names, experiment_names, season_names, site_names]):
                print(f"At least one parameter must be provided for filter.")
                return
            records = ScriptRecordModel.filter_records(
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
                script_names=script_names,
                dataset_names=dataset_names,
                experiment_names=experiment_names,
                season_names=season_names,
                site_names=site_names
            )
            for record in records:
                record = cls.model_validate(record)
                yield record
        except Exception as e:
            print(f"Error filtering ScriptRecords: {e}")
            yield None
    

    def update(
        self,
        script_data: dict = None,
        record_info: dict = None
    ) -> Optional["ScriptRecord"]:
        try:
            if not any([script_data, record_info]):
                print(f"At least one parameter must be provided for update.")
                return None
            current_id = self.id
            script_record = ScriptRecordModel.get(current_id)
            if not script_record:
                print(f"No ScriptRecord found with ID: {current_id}")
                return None
            script_record = ScriptRecordModel.update(
                script_record,
                script_data=script_data,
                record_info=record_info
            )
            script_record = self.model_validate(script_record)
            self.refresh()
            return script_record
        except Exception as e:
            print(f"Error updating ScriptRecord: {e}")
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            script_record = ScriptRecordModel.get(current_id)
            if not script_record:
                print(f"No ScriptRecord found with ID: {current_id}")
                return False
            ScriptRecordModel.delete(script_record)
            return True
        except Exception as e:
            print(f"Error deleting ScriptRecord: {e}")
            return False
        
    def refresh(self) -> Optional["ScriptRecord"]:
        try:
            db_instance = ScriptRecordModel.get(self.id)
            if not db_instance:
                print(f"No ScriptRecord found with ID: {self.id}")
                return None
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing ScriptRecord: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            script_record = ScriptRecordModel.get(current_id)
            if not script_record:
                print(f"No ScriptRecord found with ID: {current_id}")
                return None
            record_info = script_record.record_info
            if not record_info:
                print(f"No record info found for ScriptRecord with ID: {current_id}")
                return None
            return record_info
        except Exception as e:
            print(f"Error getting record info: {e}")
            return None
        
    def set_info(self, record_info: dict) -> Optional["ScriptRecord"]:
        try:
            current_id = self.id
            script_record = ScriptRecordModel.get(current_id)
            if not script_record:
                print(f"No ScriptRecord found with ID: {current_id}")
                return None
            ScriptRecordModel.update(
                script_record,
                record_info=record_info
            )
            script_record = self.model_validate(script_record)
            self.refresh()
            return script_record
        except Exception as e:
            print(f"Error setting record info: {e}")
            return None
        
    @classmethod
    def create_file_uri(cls, record: "ScriptRecord") -> Optional[str]:
        try:
            original_file_path = record.record_file
            if not original_file_path:
                print(f"record_file is required to create file URI.")
                return None
            if not os.path.exists(original_file_path):
                print(f"File {original_file_path} does not exist.")
                return None
            collection_date = record.collection_date.strftime("%Y-%m-%d")
            script_name = record.script_name
            dataset_name = record.dataset_name
            experiment_name = record.experiment_name
            season_name = record.season_name
            site_name = record.site_name
            file_extension = os.path.splitext(original_file_path)[1]
            file_timestamp = str(int(record.timestamp.timestamp() * 1000))
            file_key = f"script_data/{experiment_name}/{script_name}/{dataset_name}/{collection_date}/{site_name}/{season_name}/{file_timestamp}{file_extension}"
            return file_key
        except Exception as e:
            print(f"Error creating file URI: {e}")
            return None


    @classmethod
    def process_record(cls, record: "ScriptRecord") -> "ScriptRecord":
        try:
            file = record.record_file
            if not file:
                print(f"record_file is required to process ScriptRecord.")
                return record
            file_key = cls.create_file_uri(record)
            if not file_key:
                print(f"Failed to create file URI for ScriptRecord: {record}")
                return record
            content_type, _ = mimetypes.guess_type(file)
            # Generate Metadata for upload
            file_metadata = {
                "Script-Name": record.script_name,
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
            print(f"Error processing ScriptRecord: {e}")
            return record

