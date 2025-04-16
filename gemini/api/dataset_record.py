from typing import Optional, List, Generator
from uuid import UUID
import os, mimetypes
from tqdm import tqdm

from gemini.api.types import ID
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, FileHandlerMixin
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.columnar.dataset_records import DatasetRecordModel
from gemini.db.models.views.dataset_records_immv import DatasetRecordsIMMVModel
from gemini.db.models.views.validation_views import ValidDatasetCombinationsViewModel
from gemini.db.models.views.experiment_views import (
    ExperimentDatasetsViewModel,
    ExperimentSeasonsViewModel,
    ExperimentSitesViewModel
)

from gemini.db.models.experiments import ExperimentModel

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
    def exists(
        cls,
        timestamp: datetime,
        dataset_name: str,
        experiment_name: str,
        season_name: str,
        site_name: str,
    ) -> bool:
        try:
            exists = DatasetRecordModel.exists(
                timestamp=timestamp,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            return exists
        except Exception as e:
            raise e
   
    @classmethod
    def create(
        cls,
        timestamp: datetime = datetime.now(),
        collection_date: date = None,
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
            
            record = DatasetRecord(
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
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            dataset_record = DatasetRecordModel.get(current_id)
            DatasetRecordModel.delete(dataset_record)
            return True
        except Exception as e:
            raise False

    @classmethod
    def get_all(cls, limit: int = 100) -> List['DatasetRecord']:
        try:
            records = DatasetRecordModel.all(limit=limit)
            records = [cls.model_validate(record) for record in records]
            return records if records else None
        except Exception as e:
            raise e

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> 'DatasetRecord':
        try:
            record = DatasetRecordsIMMVModel.get(id)
            if not record:
                return None
            record = cls.model_construct(
                _fields_set=cls.model_fields_set,
                **record.to_dict()
            )
            record = record.model_dump()
            # record = cls._postprocess_record(record)
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
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e

    def update(
        self,
        dataset_data: dict = None,
        record_info: dict = None,
    ) -> 'DatasetRecord':
        try:

            # If none of the parameters are provided, raise an error
            if not dataset_data and not record_info:
                raise ValueError("At least one parameter must be provided.")
            current_id = self.id
            record = DatasetRecordModel.get(current_id)
            record = DatasetRecordModel.update(
                record,
                dataset_data=dataset_data,
                record_info=record_info
            )
            record = self.model_validate(record)
            self.refresh()
            return record
        except Exception as e:
            raise
    
    @classmethod
    def add(cls, records: List['DatasetRecord']) -> tuple[bool, List[str]]:
        try:
            records = cls._verify_records(records)
            records = [cls._preprocess_record(record) for record in tqdm(records, desc="Processing Records for Dataset: " + records[0].dataset_name)]
            records_to_insert = []
            for record in records:
                record_to_insert = record.model_dump()
                record_to_insert = {k: v for k, v in record_to_insert.items() if v is not None}
                records_to_insert.append(record_to_insert)
            print(f"Inserting Records for Dataset: {records[0].dataset_name}")
            inserted_record_ids = DatasetRecordModel.insert_bulk('dataset_records_unique', records_to_insert)
            print(f"Inserted {len(inserted_record_ids)} Records for Dataset: {records[0].dataset_name}")
            return True, inserted_record_ids
        except Exception as e:
            return False, []


    @classmethod
    def get(cls, dataset_record_id: ID) -> 'DatasetRecord':
        try:
            db_instance = DatasetRecordModel.get(dataset_record_id)
            record = cls.model_validate(db_instance)
            return record if record else None
        except Exception as e:
            raise e
        
    def get_record_info(self) -> dict:
        try:
            if not self.id:
                raise ValueError("Record ID is required to get the record info.")
            record = DatasetRecordModel.get(self.id)
            record_info = record.record_info
            return record_info if record_info else None
        except Exception as e:
            raise e
        
    def set_record_info(self, record_info: dict) -> 'DatasetRecord':
        try:
            if not self.id:
                raise ValueError("Record ID is required to set the record info.")
            record = DatasetRecordModel.get(self.id)
            DatasetRecordModel.update(record, record_info=record_info)
            self.refresh()
            return self
        except Exception as e:
            raise e

    @classmethod
    def search(
        cls,
        dataset_name: str = None,
        dataset_data: dict = None,
        experiment_name: str = None,    
        season_name: str = None,
        site_name: str = None,
        collection_date: date = None,
        record_info: dict = None,
    ) -> Generator['DatasetRecord', None, None]:
        try:

            if not any([dataset_name, dataset_data, experiment_name, season_name, site_name, collection_date, record_info]):
                raise ValueError("At least one parameter must be provided.")

            records = DatasetRecordsIMMVModel.stream(
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                collection_date=collection_date,
                dataset_data=dataset_data,
                record_info=record_info
            )

            for record in records:
                record = cls.model_construct(
                    _fields_set=cls.model_fields_set,
                    **record.to_dict()
                )
                record = record.model_dump()
                # record = cls._postprocess_record(record)
                record = cls.model_validate(record)
                yield record
        except Exception as e:
            raise e
        
    def set_experiment(self, experiment_name: str) -> 'DatasetRecord':
        try:
            record = DatasetRecordModel.get(self.id)
            experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
            DatasetRecordModel.update(record, experiment_id=experiment.id, experiment_name=experiment_name)
            self.refresh()
            return self
        except Exception as e:
            raise e
        

    def set_season(self, season_name: str) -> 'DatasetRecord':
        try:
            record = DatasetRecordModel.get(self.id)
            experiment = ExperimentModel.get(record.experiment_id)
            season = ExperimentSeasonsViewModel.get_by_parameters(
                season_name=season_name,
                experiment_name=experiment.experiment_name
            )
            DatasetRecordModel.update(record, season_id=season.season_id, season_name=season_name)
            self.refresh()
            return self
        except Exception as e:
            raise e
        
        
    def set_site(self, site_name: str) -> 'DatasetRecord':
        try:
            record = DatasetRecordModel.get(self.id)
            experiment = ExperimentModel.get(record.experiment_id)
            site = ExperimentSitesViewModel.get_by_parameters(
                site_name=site_name,
                experiment_name=experiment.experiment_name
            )
            DatasetRecordModel.update(record, site_id=site.site_id, site_name=site_name)
            self.refresh()
            return self
        except Exception as e:
            raise e
        
    def get_record_file(self, download_folder: str) -> str:
        try:
            if not self.id:
                raise ValueError("Record ID is required to get the record file.")
            record = DatasetRecordModel.get(self.id)
            if not record.record_file:
                raise ValueError("Record file is not set.")
            file_path = os.path.join(download_folder, record.record_file)
            if not os.path.exists(file_path):
                file_path = self._download_file(download_folder)
            return file_path
        except Exception as e:
            raise e


    @classmethod
    def get_valid_combinations(
        cls,
        dataset_name : str = None,
        experiment_name : str = None,
        season_name : str = None,
        site_name : str = None
    )  -> List[dict]:
        try:
            valid_combinations = ValidDatasetCombinationsViewModel.search(
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            valid_combinations = [record.to_dict() for record in valid_combinations]
            return valid_combinations if valid_combinations else None
        except Exception as e:
            raise e

        
    @classmethod
    def _verify_records(cls, records: List['DatasetRecord']) -> List['DatasetRecord']:
        try:
            
            # Refresh all the views
            ExperimentDatasetsViewModel.refresh()
            ExperimentSeasonsViewModel.refresh()
            ExperimentSitesViewModel.refresh()

            # Variables
            dataset = None
            experiments = {}
            seasons = {}
            sites = {}

            # Get all the records
           
            for record in records:
                if not record.timestamp:
                    raise ValueError("Timestamp is required.")
                if not record.collection_date:
                    record.collection_date = record.timestamp.date()
                if dataset and dataset.dataset_name != record.dataset_name:
                    raise ValueError("You can only add records for one dataset at a time.")
                
                if not dataset and DatasetModel.exists(dataset_name=record.dataset_name):
                    dataset = DatasetModel.get_by_parameters(dataset_name=record.dataset_name)

                record.dataset_id = dataset.id

                if record.experiment_name not in experiments and ExperimentDatasetsViewModel.exists(experiment_name=record.experiment_name, dataset_name=record.dataset_name):
                    experiments[record.experiment_name] = ExperimentDatasetsViewModel.get_by_parameters(experiment_name=record.experiment_name, dataset_name=record.dataset_name)

                record.experiment_id = experiments[record.experiment_name].experiment_id

                if record.season_name not in seasons and ExperimentSeasonsViewModel.exists(season_name=record.season_name, experiment_name=record.experiment_name):
                    seasons[record.season_name] = ExperimentSeasonsViewModel.get_by_parameters(season_name=record.season_name, experiment_name=record.experiment_name)

                record.season_id = seasons[record.season_name].season_id

                if record.site_name not in sites and ExperimentSitesViewModel.exists(site_name=record.site_name, experiment_name=record.experiment_name):
                    sites[record.site_name] = ExperimentSitesViewModel.get_by_parameters(site_name=record.site_name, experiment_name=record.experiment_name)

                record.site_id = sites[record.site_name].site_id

            return records
        except Exception as e:
            raise e




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
            content_type, _ = mimetypes.guess_type(absolute_file_path)
            uploaded_file_url = cls.minio_storage_provider.upload_file(
                object_name=file_key,
                input_file_path=absolute_file_path,
                bucket_name="gemini",
                content_type=content_type
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
                file_path=output_file_path,
                bucket_name="gemini"
            )
            return downloaded_file_path
        except Exception as e:
            raise e


    @classmethod
    def _get_file_download_url(cls, record_file_key: str) -> str:
        try:
            # Check if record_file is a file key or a file url
            if record_file_key.startswith("http"):
                return record_file_key
            file_url = cls.minio_storage_provider.get_download_url(object_name=record_file_key, bucket_name="gemini")
            return file_url
        except Exception as e:
            raise e



    @classmethod
    def _create_file_uri(cls, record: 'DatasetRecord') -> str:
        try:
            file_path = record.record_file
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File {file_path} does not exist.")
            collection_date = record.collection_date.strftime("%Y-%m-%d")
            dataset_name = record.dataset_name
            experiment_name = record.experiment_name
            season_name = record.season_name
            site_name = record.site_name
            file_extension = os.path.splitext(file_path)[1]
            file_timestamp = str(int(record.timestamp.timestamp()*1000))
            file_key = f"dataset_data/{experiment_name}/{dataset_name}/{collection_date}/{site_name}/{season_name}/{file_timestamp}{file_extension}"
            return file_key
        except Exception as e:
            raise e

