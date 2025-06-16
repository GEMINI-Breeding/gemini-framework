from typing import Optional, List, Generator
import os, mimetypes
from uuid import UUID
from tqdm import tqdm

from gemini.api.types import ID
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, FileHandlerMixin
from gemini.api.dataset import Dataset, GEMINIDatasetType
from gemini.db.models.procedures import ProcedureModel
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.columnar.procedure_records import ProcedureRecordModel
from gemini.db.models.views.procedure_records_immv import ProcedureRecordsIMMVModel
from gemini.db.models.views.dataset_views import ProcedureDatasetsViewModel
from gemini.db.models.views.validation_views import ValidProcedureDatasetCombinationsViewModel
from gemini.db.models.views.experiment_views import (
    ExperimentProceduresViewModel,
    ExperimentDatasetsViewModel,
    ExperimentSitesViewModel,
    ExperimentSeasonsViewModel
)


from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.associations import ProcedureDatasetModel

from datetime import date, datetime

class ProcedureRecord(APIBase, FileHandlerMixin):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "procedure_record_id"))
    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id: Optional[ID] = None
    dataset_name: Optional[str] = None
    procedure_id: Optional[ID] = None
    procedure_name: Optional[str] = None
    procedure_data: Optional[dict] = None
    experiment_id: Optional[ID] = None
    experiment_name : Optional[str] = None
    season_id: Optional[ID] = None
    season_name: Optional[str] = None
    site_id: Optional[ID] = None
    site_name: Optional[str] = None
    record_file: Optional[str] = None
    record_info: Optional[dict] = None

    def __str__(self):
        return f"ModelRecord(id={self.id}, timestamp={self.timestamp}, procedure_name={self.procedure_name}, dataset_name={self.dataset_name}, experiment_name={self.experiment_name}, site_name={self.site_name}, season_name={self.season_name})"
    
    def __repr__(self):
        return f"ModelRecord(id={self.id}, timestamp={self.timestamp}, procedure_name={self.procedure_name}, dataset_name={self.dataset_name}, experiment_name={self.experiment_name}, site_name={self.site_name}, season_name={self.season_name})"
    
    @classmethod
    def exists(
        cls,
        timestamp: datetime,
        procedure_name: str,
        dataset_name: str,
        experiment_name: str,
        season_name: str,
        site_name: str
    ) -> bool:
        try:
            exists = ProcedureRecordModel.exists(
                timestamp=timestamp,
                procedure_name=procedure_name,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            return exists
        except Exception as e:
            print(f"Error checking existence of ProcedureRecord: {e}")
            raise e
        
    @classmethod
    def create(
        cls,
        timestamp: datetime = datetime.now(),
        collection_date: date = None,
        dataset_name: str = None,
        procedure_name: str = None,
        procedure_data: dict = {},
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        record_file: str = None,
        record_info: dict = {},
        insert_on_create: bool = True
    ) -> Optional["ProcedureRecord"]:
        try:
            if not any([experiment_name, site_name, season_name]):
                raise ValueError("At least one of experiment_name, site_name, or season_name must be provided.")
            if not procedure_name:
                raise ValueError("Procedure name is required.")
            if not dataset_name:
                raise ValueError("Dataset name is required.")
            if not timestamp:
                raise ValueError("Timestamp is required.")
            if not collection_date:
                collection_date = timestamp.date()
            if not procedure_data and not record_file:
                raise ValueError("At least one of procedure_data or record_file must be provided.")
            procedure_record = ProcedureRecord(
                timestamp=timestamp,
                collection_date=collection_date,
                dataset_name=dataset_name,
                procedure_name=procedure_name,
                procedure_data=procedure_data,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                record_file=record_file,
                record_info=record_info
            )
            if insert_on_create:
                insert_success, inserted_record_ids = cls.insert([procedure_record])
                if not insert_success:
                    print(f"Failed to insert ProcedureRecord: {procedure_record}")
                    return None
                if not inserted_record_ids or len(inserted_record_ids) == 0:
                    print(f"No new ProcedureRecord was inserted.")
                    return None
                inserted_record_id = inserted_record_ids[0]
                procedure_record = cls.get_by_id(inserted_record_id)
            return procedure_record
        except Exception as e:
            print(f"Error creating ProcedureRecord: {e}")
            raise None
        
    @classmethod
    def insert(cls, records: List["ProcedureRecord"]) -> tuple[bool, List[str]]:
        try:
            if not records or len(records) == 0:
                print(f"No records provided for insertion.")
                return False, []
            records = [cls.process_record(record) for record in tqdm(records, desc="Processing ProcedureRecords")]
            records_to_insert = []
            for record in records:
                record_dict = record.model_dump()
                record_dict = {k: v for k, v in record_dict.items() if v is not None}
                records_to_insert.append(record_dict)
            print(f"Inserting {len(records_to_insert)} records.")
            inserted_record_ids = ProcedureRecordModel.insert_bulk('procedure_records_unique', records_to_insert)
            print(f"Inserted {len(inserted_record_ids)} records.")
            return True, inserted_record_ids
        except Exception as e:
            print(f"Error inserting ProcedureRecords: {e}")
            return False, []
        
    @classmethod
    def get(
        cls,
        timestamp: datetime,
        procedure_name: str,
        dataset_name: str,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None
    ) -> Optional["ProcedureRecord"]:
        try:
            if not timestamp:
                print(f"Timestamp is required to get ProcedureRecord.")
                return None
            if not dataset_name:
                print(f"Dataset name is required to get ProcedureRecord.")
                return None
            if not procedure_name:
                print(f"Procedure name is required to get ProcedureRecord.")
                return None
            if not experiment_name and not season_name and not site_name:
                print(f"At least one of experiment_name, season_name, or site_name is required to get ProcedureRecord.")
                return None
            procedure_record = ProcedureRecordsIMMVModel.get_by_parameters(
                timestamp=timestamp,
                procedure_name=procedure_name,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            if not procedure_record:
                print(f"No ProcedureRecord found for the given parameters.")
                return None
            procedure_record = cls.model_validate(procedure_record)
            return procedure_record
        except Exception as e:
            print(f"Error getting ProcedureRecord: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["ProcedureRecord"]:
        try:
            db_instance = ProcedureRecordModel.get(id)
            if not db_instance:
                print(f"No ProcedureRecord found with ID: {id}")
                return None
            record = cls.model_validate(db_instance)
            return record
        except Exception as e:
            print(f"Error getting ProcedureRecord by ID: {e}")
            return None
        
    @classmethod
    def get_all(cls, limit: int = 100) -> Optional[List["ProcedureRecord"]]:
        try:
            records = ProcedureRecordModel.all(limit=limit)
            if not records or len(records) == 0:
                print(f"No ProcedureRecords found.")
                return None
            records = [cls.model_validate(record) for record in records]
            return records
        except Exception as e:
            print(f"Error getting all ProcedureRecords: {e}")
            return None
        
    @classmethod
    def search(
        cls,
        procedure_name: str = None,
        procedure_data: dict = None,
        dataset_name: str = None,
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        collection_date: date = None,
        record_info: dict = None
    ) -> Generator["ProcedureRecord", None, None]:
        try:
            if not any([procedure_name, dataset_name, experiment_name, site_name, season_name, collection_date, record_info]):
                print(f"At least one parameter must be provided for search.")
                return
            records = ProcedureRecordsIMMVModel.stream(
                procedure_name=procedure_name,
                procedure_data=procedure_data,
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
            print(f"Error searching ProcedureRecords: {e}")
            yield None


    @classmethod
    def filter(
        cls,
        procedure_names: List[str] = None,
        dataset_names: List[str] = None,
        start_timestamp: datetime = None,
        end_timestamp: datetime = None,
        experiment_names: List[str] = None,
        site_names: List[str] = None,
        season_names: List[str] = None
    ) -> Generator["ProcedureRecord", None, None]:
        try:
            if not any([procedure_names, dataset_names, start_timestamp, end_timestamp, experiment_names, site_names, season_names]):
                print(f"At least one parameter must be provided for filtering.")
                return
            records = ProcedureRecordModel.filter_records(
                procedure_names=procedure_names,
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
            print(f"Error filtering ProcedureRecords: {e}")
            yield None

    def update(
        self,
        procedure_data: dict = None,
        record_info: dict = None
    ) -> Optional["ProcedureRecord"]:
        try:
            if not any([procedure_data, record_info]):
                print(f"At least one parameter must be provided for update.")
                return None
            current_id = self.id
            procedure_record = ProcedureRecordModel.get(current_id)
            if not procedure_record:
                print(f"No ProcedureRecord found with ID: {current_id}")
                return None
            procedure_record = ProcedureRecordModel.update(
                procedure_record,
                procedure_data=procedure_data,
                record_info=record_info
            )
            procedure_record = self.model_validate(procedure_record)
            self.refresh()
            return procedure_record
        except Exception as e:
            print(f"Error updating ProcedureRecord: {e}")
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            procedure_record = ProcedureRecordModel.get(current_id)
            if not procedure_record:
                print(f"No ProcedureRecord found with ID: {current_id}")
                return False
            ProcedureRecordModel.delete(procedure_record)
            return True
        except Exception as e:
            print(f"Error deleting ProcedureRecord: {e}")
            return False
        
    def refresh(self) -> Optional["ProcedureRecord"]:
        try:
            db_instance = ProcedureRecordModel.get(self.id)
            if not db_instance:
                print(f"No ProcedureRecord found with ID: {self.id}")
                return None
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing ProcedureRecord: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            procedure_record = ProcedureRecordModel.get(current_id)
            if not procedure_record:
                print(f"No ProcedureRecord found with ID: {current_id}")
                return None
            record_info = procedure_record.record_info
            if not record_info:
                print(f"No record info found for ProcedureRecord with ID: {current_id}")
                return None
            return record_info
        except Exception as e:
            print(f"Error getting record info: {e}")
            return None
        
    def set_info(self, record_info: dict) -> Optional["ProcedureRecord"]:
        try:
            current_id = self.id
            procedure_record = ProcedureRecordModel.get(current_id)
            if not procedure_record:
                print(f"No ProcedureRecord found with ID: {current_id}")
                return None
            ProcedureRecordModel.update(
                procedure_record,
                record_info=record_info
            )
            procedure_record = self.model_validate(procedure_record)
            self.refresh()
            return procedure_record
        except Exception as e:
            print(f"Error setting record info: {e}")
            return None
        
    @classmethod
    def create_file_uri(cls, record: "ProcedureRecord") -> Optional[str]:
        try:
            original_file_path = record.record_file
            if not original_file_path:
                print(f"record_file is required to create file URI.")
                return None
            if not os.path.exists(original_file_path):
                print(f"File {original_file_path} does not exist.")
                return None
            collection_date = record.collection_date.strftime("%Y-%m-%d")
            procedure_name = record.procedure_name
            dataset_name = record.dataset_name
            experiment_name = record.experiment_name
            season_name = record.season_name
            site_name = record.site_name
            file_extension = os.path.splitext(original_file_path)[1]
            file_timestamp = str(int(record.timestamp.timestamp() * 1000))
            file_key = f"procedure_data/{experiment_name}/{procedure_name}/{dataset_name}/{collection_date}/{site_name}/{season_name}/{file_timestamp}{file_extension}"
            return file_key
        except Exception as e:
            print(f"Error creating file URI: {e}")
            return None


    @classmethod
    def process_record(cls, record: "ProcedureRecord") -> "ProcedureRecord":
        try:
            file = record.record_file
            if not file:
                print(f"record_file is required to process ProcedureRecord.")
                return record
            file_key = cls.create_file_uri(record)
            if not file_key:
                print(f"Failed to create file URI for ProcedureRecord: {record}")
                return record
            content_type, _ = mimetypes.guess_type(file)
            # Generate Metadata for upload
            file_metadata = {
                "Procedure-Name": record.procedure_name,
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
            print(f"Error processing ProcedureRecord: {e}")
            return record

