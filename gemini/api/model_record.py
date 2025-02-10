from typing import Optional, List, Generator
import os

from gemini.api.types import ID
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, FileHandlerMixin
from gemini.db.models.models import ModelModel
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.columnar.model_records import ModelRecordModel
from gemini.db.models.views.model_records_immv import ModelRecordsIMMVModel

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

    @classmethod
    def create(
        cls,
        timestamp: datetime = datetime.now(),
        collection_date: date = date.today(),
        dataset_id: ID = None,
        dataset_name: str = None,
        model_id: ID = None,
        model_name: str = None,
        model_data: dict = {},
        experiment_id: ID = None,
        experiment_name: str = 'Default',
        site_id: ID = None,
        site_name: str = 'Default',
        season_id: ID = None,
        season_name: str = 'Default',
        record_file: str = None,
        record_info: dict = {}
    ) -> 'ModelRecord':
        try:
            record = ModelRecord.model_construct(
                _fields_set=ModelRecord.model_fields_set,
                timestamp=timestamp,
                collection_date=collection_date,
                dataset_id=dataset_id,
                dataset_name=dataset_name,
                model_id=model_id,
                model_name=model_name,
                model_data=model_data,
                experiment_id=experiment_id,
                experiment_name=experiment_name,
                site_id=site_id,
                site_name=site_name,
                season_id=season_id,
                season_name=season_name,
                record_file=record_file,
                record_info=record_info
            )
            return record
        except Exception as e:
            raise e
    
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
    def add(cls, records: List['ModelRecord']):
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
                    'model_id': record.model_id,
                    'model_name': record.model_name,
                    'model_data': record.model_data,
                    'experiment_id': record.experiment_id,
                    'experiment_name': record.experiment_name,
                    'site_id': record.site_id,
                    'site_name': record.site_name,
                    'season_id': record.season_id,
                    'season_name': record.season_name,
                    'record_file': record.record_file,
                    'record_info': record.record_info
                }
                records_to_insert.append(record_to_insert)
            ModelRecordModel.insert_bulk('model_records_unique', records_to_insert)
            return True
        except Exception as e:
            return False
        
    @classmethod
    def get(cls, model_record_id: ID) -> 'ModelRecord':
        try:
            db_instance = ModelRecordModel.get(model_record_id)
            record = cls.model_validate(db_instance)
            return record
        except Exception as e:
            raise e
        
    @classmethod
    def search(cls, **kwargs) -> Generator['ModelRecord', None, None]:
        try:
            records = ModelRecordsIMMVModel.stream(**kwargs)
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
    def _preprocess_record(cls, record: 'ModelRecord') -> 'ModelRecord':
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
            record = ModelRecordModel.get(self.id)
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
    def _create_file_uri(cls, record: 'ModelRecord') -> str:
        try:
            file_path = record.record_file
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File {file_path} does not exist.")
            file_name = os.path.basename(file_path)
            collection_date = record.collection_date.strftime("%Y-%m-%d")
            model_name = record.model_name
            file_key = f"model_data/{model_name}/{collection_date}/{file_name}"
            return file_key
        except Exception as e:
            raise e
