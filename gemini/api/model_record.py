from typing import Optional, List, Generator
import os, mimetypes
from uuid import UUID
from tqdm import tqdm

from gemini.api.types import ID
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, FileHandlerMixin
from gemini.api.dataset import Dataset, GEMINIDatasetType
from gemini.db.models.models import ModelModel
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.columnar.model_records import ModelRecordModel
from gemini.db.models.views.model_records_immv import ModelRecordsIMMVModel
from gemini.db.models.views.dataset_views import ModelDatasetsViewModel
from gemini.db.models.views.validation_views import ValidModelDatasetCombinationsViewModel
from gemini.db.models.views.experiment_views import (
    ExperimentModelsViewModel,
    ExperimentDatasetsViewModel,
    ExperimentSeasonsViewModel,
    ExperimentSitesViewModel,
)

from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.associations import ModelDatasetModel

from datetime import date, datetime

class ModelRecord(APIBase, FileHandlerMixin):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "model_record_id"))

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id: Optional[ID] = None
    dataset_name: Optional[str] = None
    model_id: Optional[ID] = None
    model_name: Optional[str] = None
    model_data: Optional[dict] = None
    experiment_id: Optional[ID] = None
    experiment_name : Optional[str] = None
    season_id: Optional[ID] = None
    season_name: Optional[str] = None
    site_id: Optional[ID] = None
    site_name: Optional[str] = None
    record_file: Optional[str] = None
    record_info: Optional[dict] = None

    def __str__(self):
        return f"ModelRecord(id={self.id}, timestamp={self.timestamp}, model_name={self.model_name}, dataset_name={self.dataset_name}, experiment_name={self.experiment_name}, site_name={self.site_name}, season_name={self.season_name})"
    
    def __repr__(self):
        return f"ModelRecord(id={self.id}, timestamp={self.timestamp}, model_name={self.model_name}, dataset_name={self.dataset_name}, experiment_name={self.experiment_name}, site_name={self.site_name}, season_name={self.season_name})"
    
    @classmethod
    def exists(
        cls,
        timestamp: datetime,
        model_name: str,
        dataset_name: str,
        experiment_name: str,
        season_name: str,
        site_name: str
    ) -> bool:
        try:
            exists = ModelRecordModel.exists(
                timestamp=timestamp,
                model_name=model_name,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            return exists
        except Exception as e:
            print(f"Error checking existence of ModelRecord: {e}")
            return False
        
    @classmethod
    def create(
        cls,
        timestamp: datetime = datetime.now(),
        collection_date: date = None,
        dataset_name: str = None,
        model_name: str = None,
        model_data: dict = {},
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        record_file: str = None,
        record_info: dict = {},
        insert_on_create: bool = True
    ) -> Optional["ModelRecord"]:
        try:
            if not any([experiment_name, site_name, season_name]):
                raise ValueError("At least one of experiment_name, site_name, or season_name must be provided.")
            if not model_name:
                raise ValueError("Model name is required.")
            if not dataset_name:
                raise ValueError("Dataset name is required.")
            if not timestamp:
                raise ValueError("Timestamp is required.")
            if not collection_date:
                collection_date = timestamp.date()
            if not model_data and not record_file:
                raise ValueError("At least one of model_data or record_file must be provided.")
            model_record = ModelRecord(
                timestamp=timestamp,
                collection_date=collection_date,
                dataset_name=dataset_name,
                model_name=model_name,
                model_data=model_data,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                record_file=record_file,
                record_info=record_info
            )
            if insert_on_create:
                insert_success, inserted_record_ids = cls.insert([model_record])
                if not insert_success:
                    print(f"Failed to insert ModelRecord: {model_record}")
                    return None
                if not inserted_record_ids or len(inserted_record_ids) == 0:
                    print(f"No new ModelRecord was inserted.")
                    return None
                inserted_record_id = inserted_record_ids[0]
                model_record = cls.get_by_id(inserted_record_id)
            return model_record
        except Exception as e:
            print(f"Error creating ModelRecord: {e}")
            raise None
        
    @classmethod
    def insert(cls, records: List["ModelRecord"]) -> tuple[bool, List[str]]:
        try:
            if not records or len(records) == 0:
                print(f"No records provided for insertion.")
                return False, []
            records = [cls.process_record(record) for record in tqdm(records, desc="Processing ModelRecords")]
            records_to_insert = []
            for record in records:
                record_dict = record.model_dump()
                record_dict = {k: v for k, v in record_dict.items() if v is not None}
                records_to_insert.append(record_dict)
            print(f"Inserting {len(records_to_insert)} records.")
            inserted_record_ids = ModelRecordModel.insert_bulk('model_records_unique', records_to_insert)
            print(f"Inserted {len(inserted_record_ids)} records.")
            return True, inserted_record_ids
        except Exception as e:
            print(f"Error inserting ModelRecords: {e}")
            return False, []
        
    @classmethod
    def get(
        cls,
        timestamp: datetime,
        model_name: str,
        dataset_name: str,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None
    ) -> Optional["ModelRecord"]:
        try:
            if not timestamp:
                print(f"Timestamp is required to get ModelRecord.")
                return None
            if not dataset_name:
                print(f"Dataset name is required to get ModelRecord.")
                return None
            if not model_name:
                print(f"Model name is required to get ModelRecord.")
                return None
            if not experiment_name and not season_name and not site_name:
                print(f"At least one of experiment_name, season_name, or site_name is required to get ModelRecord.")
                return None
            model_record = ModelRecordsIMMVModel.get_by_parameters(
                timestamp=timestamp,
                model_name=model_name,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            if not model_record:
                print(f"No ModelRecord found for the given parameters.")
                return None
            model_record = cls.model_validate(model_record)
            return model_record
        except Exception as e:
            print(f"Error getting ModelRecord: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["ModelRecord"]:
        try:
            db_instance = ModelRecordModel.get(id)
            if not db_instance:
                print(f"No ModelRecord found with ID: {id}")
                return None
            record = cls.model_validate(db_instance)
            return record
        except Exception as e:
            print(f"Error getting ModelRecord by ID: {e}")
            return None
        
    @classmethod
    def get_all(cls, limit: int = 100) -> Optional[List["ModelRecord"]]:
        try:
            records = ModelRecordModel.all(limit=limit)
            if not records or len(records) == 0:
                print(f"No ModelRecords found.")
                return None
            records = [cls.model_validate(record) for record in records]
            return records
        except Exception as e:
            print(f"Error getting all ModelRecords: {e}")
            return None
        
    @classmethod
    def search(
        cls,
        model_name: str = None,
        model_data: dict = None,
        dataset_name: str = None,
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        collection_date: date = None,
        record_info: dict = None
    ) -> Generator["ModelRecord", None, None]:
        try:
            if not any([model_name, dataset_name, experiment_name, site_name, season_name, collection_date, record_info]):
                print(f"At least one parameter must be provided for search.")
                return
            records = ModelRecordsIMMVModel.stream(
                model_name=model_name,
                model_data=model_data,
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
            print(f"Error searching ModelRecords: {e}")
            yield None

    @classmethod
    def filter(
        cls,
        model_names: List[str] = None,
        dataset_names: List[str] = None,
        start_timestamp: datetime = None,
        end_timestamp: datetime = None,
        experiment_names: List[str] = None,
        site_names: List[str] = None,
        season_names: List[str] = None
    ) -> Generator["ModelRecord", None, None]:
        try:
            if not any([model_names, dataset_names, start_timestamp, end_timestamp, experiment_names, site_names, season_names]):
                print(f"At least one parameter must be provided for filter.")
                return
            records = ModelRecordModel.filter_records(
                model_names=model_names,
                dataset_names=dataset_names,
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
                experiment_names=experiment_names,
                site_names=site_names,
                season_names=season_names
            )
            for record in records:
                record = cls.model_validate(record)
                yield record
        except Exception as e:
            print(f"Error filtering ModelRecords: {e}")
            yield None

    def update(
        self,
        model_data: dict = None,
        record_info: dict = None
    ) -> Optional["ModelRecord"]:
        try:
            if not any([model_data, record_info]):
                print(f"At least one parameter must be provided for update.")
                return None
            current_id = self.id
            model_record = ModelRecordModel.get(current_id)
            if not model_record:
                print(f"No ModelRecord found with ID: {current_id}")
                return None
            model_record = ModelRecordModel.update(
                model_record,
                model_data=model_data,
                record_info=record_info
            )
            model_record = self.model_validate(model_record)
            self.refresh()
            return model_record
        except Exception as e:
            print(f"Error updating ModelRecord: {e}")
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            model_record = ModelRecordModel.get(current_id)
            if not model_record:
                print(f"No ModelRecord found with ID: {current_id}")
                return False
            ModelRecordModel.delete(model_record)
            return True
        except Exception as e:
            print(f"Error deleting ModelRecord: {e}")
            return False
        
    def refresh(self) -> Optional["ModelRecord"]:
        try:
            db_instance = ModelRecordModel.get(self.id)
            if not db_instance:
                print(f"No ModelRecord found with ID: {self.id}")
                return None
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing ModelRecord: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            model_record = ModelRecordModel.get(current_id)
            if not model_record:
                print(f"No ModelRecord found with ID: {current_id}")
                return None
            record_info = model_record.record_info
            if not record_info:
                print(f"No record info found for ModelRecord with ID: {current_id}")
                return None
            return record_info
        except Exception as e:
            print(f"Error getting record info: {e}")
            return None
        
    def set_info(self, record_info: dict) -> Optional["ModelRecord"]:
        try:
            current_id = self.id
            model_record = ModelRecordModel.get(current_id)
            if not model_record:
                print(f"No ModelRecord found with ID: {current_id}")
                return None
            ModelRecordModel.update(
                model_record,
                record_info=record_info
            )
            model_record = self.model_validate(model_record)
            self.refresh()
            return model_record
        except Exception as e:
            print(f"Error setting record info: {e}")
            return None
        
    @classmethod
    def create_file_uri(cls, record: "ModelRecord") -> Optional[str]:
        try:
            original_file_path = record.record_file
            if not original_file_path:
                print(f"record_file is required to create file URI.")
                return None
            if not os.path.exists(original_file_path):
                print(f"File {original_file_path} does not exist.")
                return None
            collection_date = record.collection_date.strftime("%Y-%m-%d")
            model_name = record.model_name
            dataset_name = record.dataset_name
            experiment_name = record.experiment_name
            season_name = record.season_name
            site_name = record.site_name
            file_extension = os.path.splitext(original_file_path)[1]
            file_timestamp = str(int(record.timestamp.timestamp() * 1000))
            file_key = f"model_data/{experiment_name}/{model_name}/{dataset_name}/{collection_date}/{site_name}/{season_name}/{file_timestamp}{file_extension}"
            return file_key
        except Exception as e:
            print(f"Error creating file URI: {e}")
            return None


    @classmethod
    def process_record(cls, record: "ModelRecord") -> "ModelRecord":
        try:
            file = record.record_file
            if not file:
                print(f"record_file is required to process ModelRecord.")
                return record
            file_key = cls.create_file_uri(record)
            if not file_key:
                print(f"Failed to create file URI for ModelRecord: {record}")
                return record
            content_type, _ = mimetypes.guess_type(file)
            # Generate Metadata for upload
            file_metadata = {
                "Model-Name": record.model_name,
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
            print(f"Error processing ModelRecord: {e}")
            return record

    