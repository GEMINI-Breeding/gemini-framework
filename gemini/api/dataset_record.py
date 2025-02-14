from typing import Optional, List, Generator, Set
import os

from gemini.api.types import ID
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, FileHandlerMixin
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.columnar.dataset_records import DatasetRecordModel
from gemini.db.models.views.dataset_records_immv import DatasetRecordsIMMVModel

from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.seasons import SeasonModel
from gemini.db.models.sites import SiteModel

from datetime import date, datetime

class DatasetRecord(APIBase, FileHandlerMixin):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "dataset_record_id"))

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id: Optional[ID] = None
    dataset_name: Optional[str] = None
    dataset_data: Optional[dict] = None
    experiment_name: Optional[str] = None
    experiment_id: Optional[ID] = None
    season_name: Optional[str] = None
    season_id: Optional[ID] = None
    site_name: Optional[str] = None
    site_id: Optional[ID] = None
    record_file: Optional[str] = None
    record_info: Optional[dict] = None
   
    @classmethod
    def create(
        cls,
        timestamp: datetime = datetime.now(),
        collection_date: date = date.today(),
        dataset_name: str = None,
        dataset_data: dict = {},
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        record_file: str = None,
        record_info: dict = {},
    ) -> 'DatasetRecord':
        try:

            if not dataset_name:
                raise ValueError("dataset_name is required.")
            
            if not experiment_name:
                raise ValueError("experiment_name is required.")
            
            if not site_name:
                raise ValueError("site_name is required.")
            
            if not season_name:
                raise ValueError("season_name is required.")

            record = DatasetRecord.model_construct(
                _fields_set=DatasetRecord.model_fields_set,
                timestamp=timestamp,
                collection_date=collection_date,
                dataset_name=dataset_name,
                dataset_data=dataset_data,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                record_file=record_file,
                record_info=record_info
            )
            return record
        except Exception as e:
            raise e
        
    def delete(self):
        try:
            current_id = self.id
            data_type = DatasetRecordModel.get(current_id)
            DatasetRecordModel.delete(current_id)
            return data_type
        except Exception as e:
            raise e

    @classmethod
    def get_all(cls, limit: int = 100) -> List['DatasetRecord']:
        try:
            records = DatasetRecordModel.all(limit=limit)
            records = [cls.model_validate(record) for record in records]
            return records
        except Exception as e:
            raise e

    @classmethod
    def get_by_id(cls, id) -> 'DatasetRecord':
        try:
            record = DatasetRecordsIMMVModel.get(id)
            record = cls.model_construct(
                _fields_set=cls.model_fields_set,
                **record.to_dict()
            )
            record = record.model_dump()
            record = cls._postprocess_record(record)
            record = cls.model_validate(record)
            return record
        except Exception as e:
            raise e

    def refresh(self) -> 'DatasetRecord':
        try:
            db_instance = DatasetRecordModel.get(self.id)
            instance = self.model_construct(
                _fields_set=self.model_fields_set,
                **db_instance.to_dict()
            )
            for key, value in instance.model_dump().items():
                if hasattr(self, key):
                    actual_value = getattr(instance, key)
                    setattr(self, key, actual_value)
            return self
        except Exception as e:
            raise e

    def update(
        self,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
    ) -> 'DatasetRecord':
        try:
            current_id = self.id
            record = DatasetRecordModel.get(current_id)
            record.update(
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            record = self.model_validate(record)
            record.refresh()
            return record
        except Exception as e:
            raise
    
    @classmethod
    def add(cls, records: List['DatasetRecord']):
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
                    'dataset_data': record.dataset_data,
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
            DatasetRecordModel.insert_bulk('dataset_records_unique', records_to_insert)
            return True
        except Exception as e:
            return False


    @classmethod
    def get(cls, dataset_record_id: ID) -> 'DatasetRecord':
        try:
            db_instance = DatasetRecordModel.get(dataset_record_id)
            record = cls.model_validate(db_instance)
            return record
        except Exception as e:
            raise e

    @classmethod
    def search(cls, **kwargs) -> Generator['DatasetRecord', None, None]:
        try:
            records = DatasetRecordsIMMVModel.stream(**kwargs)
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
        
    # @classmethod
    # def _verify_records(cls, records: List['DatasetRecord']) -> List['DatasetRecord']:
    #     try:
    #         experiment_names : Set[str] = set()
    #         site_names : Set[str] = set()
    #         season_names : Set[str] = set()
    #         dataset_names : Set[str] = set()

    #         for record in records:
    #             experiment_names.add(record.experiment_name)
    #             site_names.add(record.site_name)
    #             season_names.add(record.season_name)
    #             dataset_names.add(record.dataset_name)

    #             # You can only add for one dataset at a time
    #             if len(dataset_names) > 1:
    #                 raise ValueError("You can only add records for one dataset at a time.")
                
    #         # Verify that the experiments exist
    #         for experiment_name in experiment_names:
    #             if not ExperimentModel.exists(experiment_name=experiment_name):
    #                 raise ValueError(f"Experiment {experiment_name} does not exist.")
                
    #         # Verify that the sites exist
    #         for site_name in site_names:
    #             if not SiteModel.exists(site_name=site_name):
    #                 raise ValueError(f"Site {site_name} does not exist.")




    @classmethod
    def _preprocess_record(cls, record: 'DatasetRecord') -> 'DatasetRecord':
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
            record = DatasetRecordModel.get(self.id)
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
    def _create_file_uri(cls, record: 'DatasetRecord') -> str:
        try:
            file_path = record.record_file
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File {file_path} does not exist.")
            file_name = os.path.basename(file_path)
            collection_date = record.collection_date.strftime("%Y-%m-%d")
            dataset_name = record.dataset_name
            file_key = f"dataset_data/{dataset_name}/{collection_date}/{file_name}"
            return file_key
        except Exception as e:
            raise e

