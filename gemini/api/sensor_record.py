from typing import Optional, List, Any, Generator
from gemini.api.base import APIBase
from gemini.models import SensorRecordModel, SensorModel, DatasetModel
from gemini.logger import logger_service


import os
from uuid import UUID
from datetime import datetime, date
from rich.progress import track

from gemini.object_store import storage_service


class SensorRecord(APIBase):

    db_model = SensorRecordModel

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_name: Optional[str] = None
    sensor_name: Optional[str] = None
    sensor_data: Optional[dict] = None
    record_info: Optional[dict] = None

    
    @classmethod
    def create(cls, **kwargs) -> 'SensorRecord':
        record = SensorRecord.model_construct(
            _fields_set=SensorRecord.model_fields_set,
            **kwargs
        )
        return record

    @classmethod
    def add(cls, records: List['SensorRecord']) -> bool:
        try:
            records_to_insert = []
            sensor_id = SensorModel.get_by_parameters(sensor_name=records[0].sensor_name).id
            dataset_id = DatasetModel.get_or_create(dataset_name=records[0].dataset_name).id
            for record in records:
                record_to_insert = {}
                record_to_insert["timestamp"] = record.timestamp
                record_to_insert["collection_date"] = record.collection_date
                record_to_insert["dataset_id"] = dataset_id
                record_to_insert["dataset_name"] = record.dataset_name
                record_to_insert["sensor_id"] = sensor_id
                record_to_insert["sensor_name"] = record.sensor_name
                record_to_insert["sensor_data"] = record.sensor_data
                record_to_insert["record_info"] = record.record_info
                records_to_insert.append(record_to_insert)

            # Preprocess records
            for record in track(records_to_insert, description="Preprocessing Sensor Records"):
                record = cls.preprocess_record(record)

            cls.db_model.insert_bulk("sensor_records_unique", records_to_insert)
            logger_service.info(
                "API",
                f"Added {len(records)} sensor records to the database",
            )
            return True
        except Exception as e:
            logger_service.error(
                "API",
                f"Failed to add sensor records to the database",
            )
            return False
        
    @classmethod
    def get(cls, record_id: UUID) -> 'SensorRecord':
        record = cls.db_model.get_by_id(record_id)
        return cls.model_validate(record)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved information about sensor record with id {self.id}",
        )
        return self.record_info
    
    def set_info(self, record_info: Optional[dict] = None) -> 'SensorRecord':
        self.update(record_info=record_info)
        logger_service.info(
            "API",
            f"Updated information about sensor record with id {self.id}",
        )
        return self
    
    def add_info(self, record_info: Optional[dict] = None) -> 'SensorRecord':
        current_info = self.get_info()
        updated_info = {**current_info, **record_info}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Added information to sensor record with id {self.id}",
        )
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> 'SensorRecord':
        current_info = self.get_info()
        updated_info = {k: v for k, v in current_info.items() if k not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Removed information from sensor record with id {self.id}",
        )
        return self
    
    @classmethod
    def search(cls, **kwargs) -> Generator['SensorRecord', None, None]:
        searched_records = cls.db_model.stream(**kwargs)
        for record in searched_records:
            record = record.to_dict()
            record = cls.postprocess_record(record)
            record = cls.model_construct(
                _fields_set=cls.model_fields_set,
                **record
            )
            yield record

    @classmethod
    def preprocess_record(cls, record: dict) -> dict:
        sensor_data = record.get("sensor_data")
        sensor_data_copy = sensor_data.copy()
        for key, value in sensor_data_copy.items():
            if key in ["file", "file_path"]:
                file_uri = cls._upload_file(value, record)
                sensor_data["file_uri"] = file_uri
                sensor_data.pop(key)

        record["sensor_data"] = sensor_data

        logger_service.info(
            "API",
            f"Processed sensor record with id {record.get('id')}",
        )
        return record
            
    @classmethod
    def postprocess_record(cls, record: dict) -> dict:
        record_copy = record.copy()
        sensor_data = record_copy.get("sensor_data")
        if not sensor_data:
            return
        file_uri = sensor_data.get("file_uri")
        if file_uri:
            downloaded_local_file_path = cls._download_file(record_copy)
            record_copy["sensor_data"]["local_file_path"] = downloaded_local_file_path
        logger_service.info(
            "API",
            f"Post-processed sensor record with id {record_copy.get('id')}",
        )
        return record_copy

    @classmethod
    def generate_file_uri(cls, absolute_file_path: str, record: dict) -> str:
        if not os.path.exists(absolute_file_path):
            raise FileNotFoundError(f"File not found at {absolute_file_path}")

        file_name = os.path.basename(absolute_file_path)
        collection_date = record.get("collection_date").strftime("%Y-%m-%d")
        file_uri = f"sensor_data/{collection_date}/{record.get('sensor_name')}/{file_name}"
        return file_uri
        

    @classmethod
    def _upload_file(cls, absolute_file_path: str, record: dict) -> str:
        file_uri = cls.generate_file_uri(absolute_file_path, record)
        

        file_tags = {
            "sensor_name": record.get("sensor_name"),
            "dataset_name": record.get("dataset_name"),
            "collection_date": record.get("collection_date").strftime("%Y-%m-%d"),
            "experiment_name": record.get("experiment_name") if record.get("experiment_name") else None,
            "site_name": record.get("site_name") if record.get("site_name") else None,
            "season_name": record.get("season_name") if record.get("season_name") else None,
            "plot_number": record.get("plot_number") if record.get("plot_number") else None,
            "plot_row_number": record.get("plot_row_number") if record.get("plot_row_number") else None,
            "plot_column_number": record.get("plot_column_number") if record.get("plot_column_number") else None,
        }

        storage_service.upload_file(
            file_path=absolute_file_path,
            key=file_uri,
            tags=file_tags
        )

        logger_service.info(
            "API",
            f"Uploaded sensor data file for sensor record with id {record.get('id')}",
        )
        return file_uri
    
    @classmethod
    def _download_file(cls, record: dict) -> str:
        file_uri = record.get("sensor_data").get("file_uri")
        if not file_uri:
            raise ValueError("No file URI found in sensor data")

        file_path = storage_service.download_file(file_uri)
        logger_service.info(
            "API",
            f"Downloaded sensor data file for sensor record with id {record.get('id')}",
        )
        return file_path
    
    def download(self) -> str:
        self.refresh()
        file_uri = self.sensor_data.get("file_uri")
        if not file_uri:
            raise ValueError("No file URI found in sensor data")

        file_path = storage_service.download_file(file_uri)
        logger_service.info(
            "API",
            f"Downloaded sensor data file for sensor record with id {self.id}",
        )
        return file_path
