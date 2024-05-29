from typing import Optional, List, Any, Generator
from pydantic import Field, BaseModel, ConfigDict
from gemini.api.base import APIBase
from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site
from gemini.api.dataset import Dataset
from gemini.api.plot import Plot
from gemini.models import ProcedureRecordModel, ProcedureModel, DatasetModel
from gemini.logger import logger_service
from gemini.object_store import storage_service
from pydantic import BaseModel
from datetime import datetime, date

from uuid import UUID
from rich.progress import track
import os

class ProcedureRecord(APIBase):

    db_model = ProcedureRecordModel

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id: Optional[UUID] = None
    dataset_name: Optional[str] = None
    procedure_id: Optional[UUID] = None
    procedure_name: Optional[str] = None
    procedure_data: Optional[dict] = None
    record_info: Optional[dict] = None


    @classmethod
    def add(cls, records: List['ProcedureRecord']) -> bool:
        try:
            records_to_insert = []
            dataset_id = DatasetModel.get_or_create(name=records[0].dataset_name).id
            procedure_id = ProcedureModel.get_by_parameter("procedure_name", records[0].procedure_name).id
            for record in records:
                record_to_insert = {}
                record_to_insert['timestamp'] = record.timestamp
                record_to_insert['collection_date'] = record.collection_date
                record_to_insert['dataset_id'] = dataset_id
                record_to_insert['dataset_name'] = record.dataset_name
                record_to_insert['procedure_id'] = procedure_id
                record_to_insert['procedure_name'] = record.procedure_name
                record_to_insert['procedure_data'] = record.procedure_data
                record_to_insert['record_info'] = record.record_info
                records_to_insert.append(record_to_insert)
            ProcedureRecordModel.insert_bulk("procedure_records_unique", records_to_insert)
            logger_service.info(
                "API",
                f"Created {len(records)} new procedure records in the database",
            )
            return True
        except Exception as e:
            logger_service.error(
                "API",
                f"Error creating procedure records in the database",
            )
            return False
        
    @classmethod
    def get(cls, record_id: UUID) -> 'ProcedureRecord':
        record = ProcedureRecordModel.get_by_id(record_id)
        return cls.model_validate(record)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info(
            "API",
            f"Getting information of the record with id {self.id}",
        )
        return self.record_info
    
    def set_info(self, record_info: dict) -> 'ProcedureRecord':
        self.update(record_info=record_info)
        logger_service.info(
            "API",
            f"Set information of the record with id {self.id}",
        )
        return self
    
    def add_info(self, record_info: dict) -> 'ProcedureRecord':
        current_info = self.get_info()
        updated_info = {**current_info, **record_info}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Added information to the record with id {self.id}",
        )
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> 'ProcedureRecord':
        current_info = self.get_info()
        updated_info = { key: value for key, value in current_info.items() if key not in keys_to_remove }
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Removed information from the record with id {self.id}",
        )
        return self

    @classmethod
    def search(cls, **kwargs) -> Generator['ProcedureRecord', None, None]:
        searched_records = ProcedureRecordModel.search(**kwargs)
        for record in searched_records:
            record = record.to_dict()
            record = cls.postprocess_record(record)
            record = cls.model_validate(record)
            yield record

    @classmethod
    def preprocess_record(cls, record: dict) -> dict:
        procedure_data = record.get("procedure_data")
        procedure_data_copy = procedure_data.copy()
        for key, value in procedure_data_copy.items():
            if key in ["file", "file_path"]:
                file_uri = cls._upload_file(value, record)
                procedure_data["file_uri"] = file_uri
                procedure_data.pop(key)

        record["procedure_data"] = procedure_data

        logger_service.info(
            "API",
            f"Preprocessed procedure record with id {record.id}",
        )

        return record
    
    @classmethod
    def postprocess_record(cls, record: dict) -> dict:
        record_copy = record.copy()
        procedure_data = record_copy.get("procedure_data")
        if not procedure_data:
            return
        file_uri = procedure_data.get("file_uri")
        if file_uri:
            downloaded_local_file_path = cls._download_file(record_copy)
            record_copy["procedure_data"]["local_file_path"] = downloaded_local_file_path
        logger_service.info(
            "API",
            f"Postprocessed procedure record with id {record['id']}",
        )
        return record_copy
    
    @classmethod
    def generate_file_uri(cls, absolute_file_path: str, record: dict) -> str:
        if not os.path.exists(absolute_file_path):
            raise FileNotFoundError(f"File not found at {absolute_file_path}")
        
        file_name = os.path.basename(absolute_file_path)
        collection_date = record.get("collection_date").strftime("%Y-%m-%d")
        file_uri = f"sensor_data/{collection_date}/{record.get('procedure_name')}/{file_name}"
        return file_uri
    
    @classmethod
    def _upload_file(cls, absolute_file_path: str, record: dict) -> str:
        file_uri = cls.generate_file_uri(absolute_file_path, record)
        file_tags = {
            "procedure_name": record.get("procedure_name"),
            "dataset_name": record.get("dataset_name"),
            "collection_date": record.get("collection_date").strftime("%Y-%m-%d"),
            **record.get("record_info")
        }
        storage_service.upload_file(
            file_path=absolute_file_path,
            key=file_uri,
            tags=file_tags
        )

        logger_service.info(
            "API",
            f"Uploaded procedure data file for procedure record with id {record['id']}",
        )

        return file_uri
    
    @classmethod
    def _download_file(cls, record: dict) -> str:
        procedure_data = record.get("procedure_data")
        file_uri = procedure_data.get("file_uri")
        if not file_uri:
            raise ValueError("No file associated with the procedure record")
        file_path = storage_service.download_file(key=file_uri)
        logger_service.info(
            "API",
            f"Downloaded procedure data file for procedure record with id {record['id']}",
        )
        return file_path
    
    def download(self) -> str:
        self.refresh()
        file_uri = self.procedure_data.get("file_uri")
        if not file_uri:
            raise ValueError("No file associated with the procedure record")
        
        file_path = storage_service.download_file(key=file_uri)
        logger_service.info(
            "API",
            f"Downloaded procedure data file for procedure record with id {self.id}",
        )
        return file_path

