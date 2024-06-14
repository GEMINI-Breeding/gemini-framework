from typing import Optional, List, Any, Generator
from pydantic import Field, BaseModel, ConfigDict
from gemini.api.base import APIBase, ID
from gemini.models import DatasetRecordModel, DatasetModel
from gemini.logger import logger_service
from gemini.object_store import storage_service
from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID
from rich.progress import track
import os

class DatasetRecord(APIBase):

    db_model = DatasetRecordModel

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id : Optional[ID] = None
    dataset_name : Optional[str] = None
    dataset_data: Optional[dict] = None
    record_info: Optional[dict] = None

    @classmethod
    def create(cls, **kwargs):
        record = DatasetRecord.model_construct(
            _fields_set=DatasetRecord.model_fields_set,
            **kwargs
        )
        return record

    @classmethod
    def add(cls, records: List['DatasetRecord']) -> bool:
        try:
            records_to_insert = []
            dataset_id = DatasetModel.get_or_create(dataset_name=records[0].dataset_name).id
            for record in track(records, description=f"Adding {len(records)} records to the dataset"):
                record_to_insert = {}
                record_to_insert['timestamp'] = record.timestamp
                record_to_insert['collection_date'] = record.timestamp.date()
                record_to_insert['dataset_id'] = dataset_id
                record_to_insert['dataset_name'] = record.dataset_name
                record_to_insert['dataset_data'] = record.dataset_data
                record_to_insert['record_info'] = record.record_info
                records_to_insert.append(record_to_insert)

            # Preprocess records
            for record in track(records_to_insert, description="Preprocessing Dataset Records"):
                record = cls.preprocess_record(record)

            DatasetRecordModel.insert_bulk('dataset_records_unique', records_to_insert)
            logger_service.info('API', f'Added {len(records)} records to the database')
            return True
        except Exception as e:
            logger_service.error('API', f'Error adding records to the database: {e}')
            return False
        
    @classmethod
    def get(cls, record_id: ID) -> 'DatasetRecord':
        record = DatasetRecordModel.get_by_id(record_id)
        return record
    
    def set_info(self, record_info: Optional[dict] = None) -> 'DatasetRecord':
        self.update(record_info=record_info)
        logger_service.info('API', f'Set information about dataset record with id {self.id}')
        return self
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info('API', f'Retrieved information about dataset record with id {self.id}')
        return self.record_info
    
    def add_info(self, record_info: Optional[dict] = None) -> 'DatasetRecord':
        current_info = self.record_info
        updated_info = {**current_info, **record_info}
        self.set_info(updated_info)
        logger_service.info('API', f'Added information to dataset record with id {self.id}')
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> 'DatasetRecord':
        current_info = self.record_info
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info('API', f'Removed information from dataset record with id {self.id}')
        return self
    
    @classmethod
    def search(cls, **kwargs) -> Generator['DatasetRecord', None, None]:
        records = DatasetRecordModel.stream(**kwargs)
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
        dataset_data = record.get("dataset_data")
        dataset_data_copy = dataset_data.copy()
        for key, value in dataset_data_copy.items():
            if key in ["file", "file_path"]:
                file_uri = cls._upload_file(value, record)
                dataset_data["file_uri"] = file_uri
                dataset_data.pop(key)

        record["dataset_data"] = dataset_data

        logger_service.info(
            "API",
            f"Preprocessed record with id {record.get('id')}",
        )
        return record
    
    @classmethod
    def postprocess_record(cls, record: dict) -> dict:
        record_copy = record.copy()
        dataset_data = record_copy.get("dataset_data")
        if not dataset_data:
            return
        file_uri = dataset_data.get("file_uri")
        if file_uri:
            downloaded_local_file_path = cls._download_file(record_copy)
            record_copy["dataset_data"]["file_path"] = downloaded_local_file_path
        logger_service.info(
            "API",
            f"Postprocessed record with id {record.get('id')}",
        )
        return record_copy
    
    @classmethod
    def generate_file_uri(cls, file_path: str, record: dict) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at {file_path}")

        file_name = os.path.basename(file_path)
        collection_date = record.get("collection_date").strftime("%Y-%m-%d")
        file_uri = f"dataset_data/{collection_date}/{record.get('dataset_name')}/{file_name}"
        return file_uri
    
    @classmethod
    def _upload_file(cls, absolute_file_path: str, record: dict) -> str:
        file_uri = cls.generate_file_uri(absolute_file_path, record)

        file_tags = {
            "dataset_name": record.get("dataset_name"),
            "collection_date": record.get("collection_date").strftime("%Y-%m-%d"),
            "experiment_name": record.get("experiment_name") if record.get("experiment_name") else None,
            "season_name": record.get("season_name") if record.get("season_name") else None,
            "site_name": record.get("site_name") if record.get("site_name") else None,
            "plot_number": record.get("plot_number") if record.get("plot_number") else None,
            "plot_row_number": record.get("plot_row_number") if record.get("plot_row_number") else None,
            "plot_column_number": record.get("plot_column_number") if record.get("plot_column_number") else None
        }
        storage_service.upload_file(
            file_path=absolute_file_path,
            key=file_uri,
            tags=file_tags
        )

        logger_service.info(
            "API",
            f"Uploaded dataset data file for record with id {record.get('id')}",
        )

        return file_uri
    
    @classmethod
    def _download_file(cls, record: dict) -> str:
        dataset_data = record.get("dataset_data")
        file_uri = dataset_data.get("file_uri")
        if not file_uri:
            raise ValueError("No file URI found in dataset data")

        file_path = storage_service.download_file(file_uri)
        logger_service.info(
            "API",
            f"Downloaded dataset data file for record with id {record.get('id')}",
        )
        return file_path
    
    def download(self) -> str:
        self.refresh()
        file_uri = self.dataset_data.get("file_uri")
        if not file_uri:
            raise ValueError("No file URI found in dataset data")
        
        file_path = storage_service.download_file(file_uri)
        logger_service.info(
            "API",
            f"Downloaded dataset data file for record with id {self.id}",
        )
        return file_path        
