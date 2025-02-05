from typing import Optional, List, Generator
import os

from gemini.api.types import ID
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, FileHandlerMixin
from gemini.db.models.sensors import SensorModel
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.columnar.sensor_records import SensorRecordModel
from gemini.db.models.views.sensor_records_immv import SensorRecordsIMMVModel

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
    plot_number: Optional[str] = None
    plot_row_number: Optional[str] = None
    plot_column_number: Optional[str] = None
    record_file: Optional[str] = None
    record_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        timestamp: datetime = datetime.now(),
        collection_date: date = date.today(),
        dataset_id: ID = None,
        dataset_name: str = None,
        sensor_id: ID = None,
        sensor_name: str = None,
        sensor_data: dict = {},
        experiment_id: ID = None,
        experiment_name: str = 'Default',
        site_id: ID = None,
        site_name: str = 'Default',
        season_id: ID = None,
        season_name: str = 'Default',
        plot_id: ID = None,
        plot_number: str = 'Default',
        plot_row_number: str = 'Default',
        plot_column_number: str = 'Default',
        record_file: str = None,
        record_info: dict = {}
    ) -> 'SensorRecord':
        try:
            record = SensorRecord.model_construct(
                _fields_set=SensorRecord.model_fields_set,
                timestamp=timestamp,
                collection_date=collection_date,
                dataset_id=dataset_id,
                dataset_name=dataset_name,
                sensor_id=sensor_id,
                sensor_name=sensor_name,
                sensor_data=sensor_data,
                experiment_id=experiment_id,
                experiment_name=experiment_name,
                site_id=site_id,
                site_name=site_name,
                season_id=season_id,
                season_name=season_name,
                plot_id=plot_id,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                record_file=record_file,
                record_info=record_info
            )
            return record
        except Exception as e:
            raise e
        
    @classmethod
    def add(cls, records: List['SensorRecord']):
        try:
            records_to_insert = []
            dataset_id = DatasetModel.get_or_create(dataset_name=records[0].dataset_name).id
            records = [cls._preprocess_record(record) for record in records]
            for record in records:
                record_to_insert = {
                    'timestamp': record.timestamp,
                    'collection_date': record.timestamp.date(),
                    'dataset_id': dataset_id,
                    'dataset_name': record.dataset_name,
                    'sensor_id': record.sensor_id,
                    'sensor_name': record.sensor_name,
                    'sensor_data': record.sensor_data,
                    'experiment_id': record.experiment_id,
                    'experiment_name': record.experiment_name,
                    'site_id': record.site_id,
                    'site_name': record.site_name,
                    'season_id': record.season_id,
                    'season_name': record.season_name,
                    'plot_id': record.plot_id,
                    'plot_number': record.plot_number,
                    'plot_row_number': record.plot_row_number,
                    'plot_column_number': record.plot_column_number,
                    'record_file': record.record_file,
                    'record_info': record.record_info
                }
                records_to_insert.append(record_to_insert)
            SensorRecordModel.insert_bulk('sensor_records_unique', records_to_insert)
            return True
        except Exception as e:
            return False

    @classmethod
    def delete(self):
        # Implement the delete method
        pass

    @classmethod
    def get_all(cls):
        # Implement the get_all method
        pass

    @classmethod
    def get_by_id(cls, id):
        # Implement the get_by_id method
        pass

    def refresh(self):
        # Implement the refresh method
        pass

    def update(self, **kwargs):
        # Implement the update method
        pass

    @classmethod
    def get(cls, sensor_record_id: ID) -> 'SensorRecord':
        try:
            db_instance = SensorRecordModel.get(sensor_record_id)
            record = cls.model_validate(db_instance)
            return record
        except Exception as e:
            raise e
        
    @classmethod
    def search(cls, **kwargs) -> Generator['SensorRecord', None, None]:
        try:
            records = SensorRecordsIMMVModel.stream(**kwargs)
            for record in records:
                record = cls.model_construct(
                    _fields_set=cls.model_fields_set,
                    **record.to_dict()
                )
                record = record.model_dump()
                record = cls._postprocess_record(record)
                record = cls.model_validate(record)
                yield record
        except Exception as e:
            raise e
        
    @classmethod
    def _preprocess_record(cls, record: 'SensorRecord') -> 'SensorRecord':
        try:
            file = record.record_file
            if not file:
                return record            
            file_key = cls._create_file_uri(record)
            cls._upload_file(
                file_key=file_key,
                absolute_file_path=file
            )

            record.record_file = file_key
            return record
        except Exception as e:
            raise e
        
    @classmethod
    def _postprocess_record(cls, record: dict) -> dict:
        try:
            file = record.get('record_file')
            if not file:
                return record
            file_url = cls._get_file_download_url(file)
            record['record_file'] = file_url
            return record
        except Exception as e:
            raise e
        
    @classmethod
    def _upload_file(cls, file_key: str, absolute_file_path: str) -> str:
        try:
            with open(absolute_file_path, "rb") as file:
                uploaded_file_url = cls.minio_storage_provider.upload_file(
                    object_name=file_key,
                    data_stream=file
                )
                return uploaded_file_url
        except Exception as e: 
            raise e
        
    def _download_file(self, output_folder: str) -> str:
        try:
            if not self.id:
                raise ValueError("Record ID is required to download the file.")
            record = SensorRecordModel.get(self.id)
            output_file_path = os.path.join(output_folder, record.record_file)
            downloaded_file_path = self.minio_storage_provider.download_file(
                object_name=record.record_file,
                file_path=output_file_path
            )
            return downloaded_file_path
        except Exception as e:
            raise e
        
    def _get_file_download_url(self, record_file_key: str) -> str:
        try:
            # Check if record_file is a file key or a file url
            if record_file_key.startswith("http"):
                return record_file_key
            file_url = self.minio_storage_provider.get_download_url(object_name=record_file_key)
            return file_url
        except Exception as e:
            raise e
        
    @classmethod
    def _create_file_uri(cls, record: 'SensorRecord') -> str:
        try:
            file_path = record.record_file
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File {file_path} does not exist.")
            file_name = os.path.basename(file_path)
            collection_date = record.collection_date.strftime("%Y-%m-%d")
            sensor_name = record.sensor_name
            file_key = f"sensor_data/{sensor_name}/{collection_date}/{file_name}"
            return file_key
        except Exception as e:
            raise e
    