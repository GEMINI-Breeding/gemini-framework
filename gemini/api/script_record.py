from typing import Optional, List, Any, Generator
from gemini.api.base import APIBase
from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site
from gemini.api.plot import Plot
from gemini.api.script import Script
from gemini.api.dataset import Dataset
from gemini.models import ScriptModel, ScriptRunModel, DatasetModel
from gemini.logger import logger_service
from gemini.object_store import storage_service
from datetime import datetime, date

from uuid import UUID
from rich.progress import track
import os


class ScriptRecord(APIBase):

    db_model = ScriptRunModel

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id: Optional[UUID] = None
    dataset_name: Optional[str] = None
    script_id: Optional[UUID] = None
    script_name: Optional[str] = None
    script_data: Optional[dict] = None
    record_info: Optional[dict] = None

    @classmethod
    def create(cls, **kwargs) -> 'ScriptRecord':
        record = ScriptRecord.model_construct(
            _fields_set=ScriptRecord.model_fields_set,
            **kwargs
        )
        return record

    @classmethod
    def add(cls, records: List['ScriptRecord']) -> bool:
        try:
            records_to_insert = []
            script_id = ScriptModel.get_by_parameter("script_name", records[0].script_name).id
            dataset_id = DatasetModel.get_by_parameter("dataset_name", records[0].dataset_name).id
            for record in records:
                record_to_insert = {}
                record_to_insert["timestamp"] = record.timestamp
                record_to_insert["collection_date"] = record.collection_date
                record_to_insert["dataset_id"] = dataset_id
                record_to_insert["dataset_name"] = record.dataset_name
                record_to_insert["script_id"] = script_id
                record_to_insert["script_name"] = record.script_name
                record_to_insert["script_data"] = record.script_data
                record_to_insert["record_info"] = record.record_info
                records_to_insert.append(record_to_insert)
            ScriptRunModel.insert_bulk("script_runs", records_to_insert)
            logger_service.info(
                "API",
                f"Inserted {len(records)} script records into the database",
            )
            return True
        except Exception as e:
            logger_service.error(
                "API",
                f"Failed to insert script records into the database",
            )
            return False
        
    @classmethod
    def get(cls, record_id: UUID) -> 'ScriptRecord':
        record = ScriptRunModel.get_by_id(record_id)
        return cls.model_validate(record)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info(
            "API",
            f"Getting information of the record with id {self.id}",
        )
        return self.record_info
    
    def set_info(self, record_info: dict) -> 'ScriptRecord':
        self.update(record_info=record_info)
        logger_service.info(
            "API",
            f"Set information of the record with id {self.id}",
        )
        return self
    
    def add_info(self, record_info: dict) -> 'ScriptRecord':
        current_info = self.get_info()
        updated_info = {**current_info, **record_info}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Added information to the record with id {self.id}",
        )
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> 'ScriptRecord':
        current_info = self.get_info()
        updated_info = { key: value for key, value in current_info.items() if key not in keys_to_remove }
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Removed information from the record with id {self.id}",
        )

    @classmethod
    def search(cls, **kwargs) -> Generator['ScriptRecord', None, None]:
        searched_records = ScriptRunModel.stream(**kwargs)
        for record in searched_records:
            record = record.to_dict()
            record = cls.postprocess_record(record)
            record = cls.model_validate(record)
            yield record

    @classmethod
    def preprocess_record(cls, record: dict) -> dict:
        script_data = record.get("script_data")
        script_data_copy = script_data.copy()
        for key, value in script_data_copy.items():
            if key in ["file", "file_path", "script"]:
                file_uri = cls._upload_file(value, record)
                script_data["file_uri"] = file_uri
                script_data.pop(key)

        record["script_data"] = script_data

        logger_service.info(
            "API",
            f"Preprocessed the record with id {record['id']}",
        )
        return record
    
    @classmethod
    def postprocess_record(cls, record: dict) -> dict:
        record_copy = record.copy()
        script_data = record_copy.get("script_data")
        if not script_data:
            return
        file_uri = script_data.get("file_uri")
        if file_uri:
            downloaded_local_file_path = cls._download_file(record_copy)
            record_copy["script_data"]["local_file_path"] = downloaded_local_file_path
        logger_service.info(
            "API",
            f"Postprocessed the record with id {record['id']}",
        )
        return record_copy
    

    @classmethod
    def generate_file_uri(cls, absolute_file_path: str, record: dict) -> str:
        if not os.path.exists(absolute_file_path):
            raise FileNotFoundError(f"File {absolute_file_path} not found")
        
        file_name = os.path.basename(absolute_file_path)
        collection_date = record.get("collection_date").strftime("%Y-%m-%d")
        file_uri = f"script_data/{collection_date}/{record.get('script_name')}/{file_name}"
        return file_uri
    
    @classmethod
    def _upload_file(cls, absolute_file_path: str, record: dict) -> str:

        file_uri = cls.generate_file_uri(absolute_file_path, record)

        file_tags = {
            "script_name": record.get("script_name"),
            "dataset_name": record.get("dataset_name"),
            "collection_date": record.get("collection_date"),
            **record.get("record_info")
        }

        storage_service.upload_file(
            file_path=absolute_file_path,
            key=file_uri,
            tags=file_tags
        )

        logger_service.info(
            "API",
            f"Uploaded file {absolute_file_path} to {file_uri}",
        )

        return file_uri
    
    @classmethod
    def _download_file(cls, record: dict) -> str:
        file_uri = record.get("script_data").get("file_uri")
        if not file_uri:
            raise ValueError("File URI not found in the record")
        
        file_path = storage_service.download_file(file_uri)
        logger_service.info(
            "API",
            f"Downloaded file {file_uri} to {file_path}",
        )
        return file_path
    
    def download(self) -> str:
        self.refresh()
        file_uri = self.script_data.get("file_uri")
        if not file_uri:
            raise ValueError("File URI not found in the record")
        
        file_path = storage_service.download_file(file_uri)
        logger_service.info(
            "API",
            f"Downloaded file {file_uri} to {file_path}",
        )
        return file_path
    