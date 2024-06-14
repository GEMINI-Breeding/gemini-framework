from typing import Optional, List, Any, Generator
from pydantic import Field, BaseModel, ConfigDict
from gemini.api.base import APIBase, ID
from gemini.models import ModelRecordModel, DatasetModel, ModelModel
from gemini.logger import logger_service
from gemini.object_store import storage_service
from pydantic import BaseModel
from datetime import datetime, date
from rich.progress import track

import os

class ModelRecord(APIBase):

    db_model = ModelRecordModel

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id: Optional[ID] = None
    dataset_name: Optional[str] = None
    model_id: Optional[ID] = None
    model_name: Optional[str] = None
    model_data: Optional[dict] = None
    record_info: Optional[dict] = None

    @classmethod
    def create(cls, **kwargs) -> 'ModelRecord':
        record = ModelRecord.model_construct(
            _fields_set=ModelRecord.model_fields_set,
            **kwargs
        )
        return record

    @classmethod
    def add(cls, records: List['ModelRecord']) -> bool:
        try:
            records_to_insert = []
            dataset_id = DatasetModel.get_or_create(name=records[0].dataset_name).id
            model_id = ModelModel.get_or_create(name=records[0].model_name).id
            for record in records:
                record_to_insert = {}
                record_to_insert['timestamp'] = record.timestamp
                record_to_insert['collection_date'] = record.collection_date
                record_to_insert['dataset_id'] = dataset_id
                record_to_insert['dataset_name'] = record.dataset_name
                record_to_insert['model_id'] = model_id
                record_to_insert['model_name'] = record.model_name
                record_to_insert['model_data'] = record.model_data
                record_to_insert['record_info'] = record.record_info
                records_to_insert.append(record_to_insert)

            # Preprocess records
            for record in track(records_to_insert, description="Preprocessing Model Records"):
                record = cls.preprocess_record(record)
                
            ModelRecordModel.insert_bulk('model_records_unique', records_to_insert)


            logger_service.info(
                "API",
                f"Added {len(records)} model records to the database",
            )
            return True
        except Exception as e:
            logger_service.error(
                "API",
                f"Failed to add model records to the database",
            )
            return False
        
    @classmethod
    def get(cls, record_id: ID) -> 'ModelRecord':
        record = ModelRecordModel.get_by_id(record_id)
        return cls.model_validate(record)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info(
            "API",
            f"Getting information of the record with id {self.id}",
        )
        return self.record_info
    
    def set_info(self, record_info: dict) -> 'ModelRecord':
        self.update(record_info=record_info)
        logger_service.info(
            "API",
            f"Set information of the record with id {self.id}",
        )
        return self
    
    def add_info(self, record_info: dict) -> 'ModelRecord':
        current_info = self.get_info()
        updated_info = {**current_info, **record_info}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Added information to the record with id {self.id}",
        )
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> 'ModelRecord':
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Removed information from the record with id {self.id}",
        )
        return self
        
    @classmethod
    def search(cls, **kwargs) -> Generator['ModelRecord', None, None]:
        records = ModelRecordModel.stream(**kwargs)
        for record in records:
            record = record.to_dict()
            record = cls.postprocess_record(record)
            record = cls.model_construct(
                _fields_set=cls.model_fields_set,
                **record
            )
            yield record

    @classmethod
    def preprocess_record(cls, record: dict) -> dict:
        model_data = record.get("model_data")
        model_data_copy = model_data.copy()
        for key, value in model_data_copy.items():
            if key in ["file", "file_path"]:
                file_uri = cls._upload_file(value, record)
                model_data["file_uri"] = file_uri
                model_data.pop(key)

        record["model_data"] = model_data

        logger_service.info(
            "API",
            f"Preprocessed record with id {record.get('id')}",
        )
        
        return record
    
    @classmethod
    def postprocess_record(cls, record: dict) -> dict:
        record_copy = record.copy()
        model_data = record_copy.get("model_data")
        if not model_data:
            return
        
        file_uri = model_data.get("file_uri")
        if file_uri:
            downloaded_local_file_path = cls._download_file(record_copy)
            record_copy["model_data"]["local_file_path"] = downloaded_local_file_path

        logger_service.info(
            "API",
            f"Postprocessed record with id {record_copy.get('id')}",
        )
        return record_copy

    @classmethod
    def generate_file_uri(cls, absolute_file_path: str, record: dict) -> str:
        if not os.path.exists(absolute_file_path):
            raise FileNotFoundError(f"File not found at path {absolute_file_path}")

        file_name = os.path.basename(absolute_file_path)
        collection_date = record.get('collection_date').strftime('%Y-%m-%d')
        file_uri = f"model_data/{collection_date}/{record.get('model_name')}/{file_name}"
        return file_uri
    

    @classmethod
    def _upload_file(cls, absolute_file_path: str, record: dict) -> str:
        file_uri = cls.generate_file_uri(absolute_file_path, record)
        file_tags = {
            "model_name": record.get("model_name"),
            "dataset_name": record.get("dataset_name"),
            "collection_date": record.get("collection_date").strftime('%Y-%m-%d'),
            "experiment_name": record.get("experiment_name"),
            "site_name": record.get("site_name"),
            "season_name": record.get("season_name"),
            "plot_number": record.get("plot_number"),
            "plot_row_number": record.get("plot_row_number"),
            "plot_column_number": record.get("plot_column_number"),
        }

        storage_service.upload_file(file_path=absolute_file_path, key=file_uri, tags=file_tags)
        logger_service.info(
            "API",
            f"Uploaded model data file for record with id {record.get('id')}",
        )
        return file_uri
    
    @classmethod
    def _download_file(cls, record: dict) -> str:
        file_uri = record.get("model_data").get("file_uri")
        if not file_uri:
            raise ValueError("File URI not found in the record")
        
        file_path = storage_service.download_file(file_uri)
        logger_service.info(
            "API",
            f"Downloaded model data file for record with id {record.get('id')}",
        )
        return file_path
    
    def download(self) -> str:
        self.refresh()
        file_uri = self.model_data.get("file_uri")
        if not file_uri:
            raise ValueError("File URI not found in the record")
        
        file_path = storage_service.download_file(file_uri)
        logger_service.info(
            "API",
            f"Downloaded model data file for record with id {self.id}",
        )
        return file_path
