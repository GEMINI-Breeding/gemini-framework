from typing import Optional, List, Generator
import os
from uuid import UUID

from gemini.api.types import ID
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, FileHandlerMixin
from gemini.api.dataset import Dataset, GEMINIDatasetType
from gemini.db.models.scripts import ScriptModel
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.columnar.script_records import ScriptRecordModel
from gemini.db.models.views.script_records_immv import ScriptRecordsIMMVModel
from gemini.db.models.views.validation_views import ValidScriptDatasetCombinationsViewModel
from gemini.db.models.views.experiment_views import (
    ExperimentScriptsViewModel,
    ExperimentDatasetsViewModel,
    ExperimentSeasonsViewModel,
    ExperimentSitesViewModel
)

from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.datasets import DatasetModel

from datetime import date, datetime

class ScriptRecord(APIBase, FileHandlerMixin):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "script_record_id"))

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id: Optional[ID] = None
    dataset_name: Optional[str] = None
    script_id: Optional[ID] = None
    script_name: Optional[str] = None
    script_data: Optional[dict] = None
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
        dataset_name: str = None,
        script_name: str = None,
        script_data: dict = {},
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        record_file: str = None,
        record_info: dict = {}
    ) -> 'ScriptRecord':
        try:
            if not script_name:
                raise ValueError("Script name is required.")
            
            if not dataset_name:
                raise ValueError("Dataset name is required.")
            
            if not experiment_name:
                raise ValueError("Experiment name is required.")
            
            if not site_name:
                raise ValueError("Site name is required.")
            
            if not season_name:
                raise ValueError("Season name is required.")

            record = ScriptRecord(
                timestamp=timestamp,
                collection_date=collection_date,
                dataset_name=dataset_name,
                script_name=script_name,
                script_data=script_data,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                record_file=record_file,
                record_info=record_info
            )

            return record
        except Exception as e:
            raise e
        
    @classmethod
    def add(cls, records: List['ScriptRecord']) -> tuple[bool, List[str]]:
        try:
            records = cls._verify_records(records)
            records = [cls._preprocess_record(record) for record in records]
            records_to_insert = []
            for record in records:
                record_to_insert = record.model_dump()
                record_to_insert = {k: v for k, v in record_to_insert.items() if v is not None}
                records_to_insert.append(record_to_insert)
            inserted_record_ids = ScriptRecordModel.insert_bulk('script_records_unique', records_to_insert)
            return True, inserted_record_ids
        except Exception as e:
            return False, []

    def delete(self) -> bool:
        try:
            current_id = self.id
            script_record = ScriptRecordModel.get(current_id)
            ScriptRecordModel.delete(script_record)
            return True
        except Exception as e:
            return False
        
    @classmethod
    def get_all(cls, limit: int = 100) -> List["ScriptRecord"]:
        try:
            instances = ScriptRecordModel.all(limit=limit)
            records = [cls.model_validate(instance) for instance in instances]
            return records if records else None
        except Exception as e:
            raise e

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "ScriptRecord":
        try:
            record = ScriptRecordModel.get(id)
            if not record:
                return None
            record = cls.model_construct(
                _fields_set=cls.model_fields_set,
                **record.to_dict()
            )
            record = record.model_dump()
            # record = cls._postprocess_record(record)
            record = cls.model_validate(record)
            return record if record else None
        except Exception as e:
            raise e

    def refresh(self) -> "ScriptRecord":
        try:
            db_instance = ScriptRecordModel.get(self.id)
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
        script_data: dict = None,
        record_info: dict = None
    ) -> "ScriptRecord":
        try:
            if not script_data and not record_info:
                raise Exception("At least one parameter must be provided.")
            current_id = self.id
            script_record = ScriptRecordModel.get(current_id)
            script_record = ScriptRecordModel.update(
                script_record,
                script_data=script_data,
                record_info=record_info
            )
            script_record = self.model_validate(script_record)
            self.refresh()
            return script_record
        except Exception as e:
            raise e

    @classmethod
    def get(cls, script_record_id: ID) -> 'ScriptRecord':
        try:
            db_instance = ScriptRecordModel.get(script_record_id)
            record = cls.model_validate(db_instance)
            return record if record else None
        except Exception as e:
            raise e
        
    def get_record_info(self) -> dict:
        try:
            if not self.id:
                raise ValueError("Record ID is required to get the record info.")
            record = ScriptRecordModel.get(self.id)
            record_info = record.record_info
            return record_info if record_info else None
        except Exception as e:
            raise e
        
    def set_record_info(self, record_info: dict) -> "ScriptRecord":
        try:
            if not self.id:
                raise ValueError("Record ID is required to set the record info.")
            record = ScriptRecordModel.get(self.id)
            record = ScriptRecordModel.update(record, record_info=record_info)
            self.refresh()
            return self
        except Exception as e:
            raise e


    @classmethod
    def search(
        cls, 
        dataset_name: str = None,
        script_name: str = None,
        script_data: dict = None,
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        collection_date: date = None,
        record_info: dict = None
    ) -> Generator['ScriptRecord', None, None]:
        try:
            if not any([dataset_name, script_data, script_name, experiment_name, site_name, season_name, collection_date]):
                raise Exception("At least one search parameter must be provided.")

            records = ScriptRecordsIMMVModel.stream(
                dataset_name=dataset_name,
                script_name=script_name,
                script_data=script_data,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                collection_date=collection_date,
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
        
    def set_experiment(self, experiment_name: str) -> "ScriptRecord":
        try:
            record = ScriptRecordModel.get(self.id)
            experiment = ExperimentModel.get_or_create(experiment_name=experiment_name)
            record = ScriptRecordModel.update(record, experiment_id=experiment.id, experiment_name=experiment.experiment_name)
            self.refresh()
            return self
        except Exception as e:
            raise e
        
    def set_season(self, season_name: str) -> "ScriptRecord":
        try:
            record = ScriptRecordModel.get(self.id)
            experiment = ExperimentModel.get(record.experiment_id)
            season = ExperimentSeasonsViewModel.get_by_parameters(
                experiment_id=experiment.id,
                season_name=season_name
            )
            ScriptRecordModel.update(record, season_id=season.season_id, season_name=season.season_name)
            self.refresh()
            return self
        except Exception as e:
            raise e
        
    def set_site(self, site_name: str) -> "ScriptRecord":
        try:
            record = ScriptRecordModel.get(self.id)
            experiment = ExperimentModel.get(record.experiment_id)
            site = ExperimentSitesViewModel.get_by_parameters(
                experiment_id=experiment.id,
                site_name=site_name
            )
            ScriptRecordModel.update(record, site_id=site.site_id, site_name=site.site_name)
            self.refresh()
            return self
        except Exception as e:
            raise e
        
          
    def get_record_file(self, download_folder: str) -> str:
        try:
            if not self.id:
                raise ValueError("Record ID is required to get the record file.")
            record = ScriptRecordModel.get(self.id)
            if not record.record_file:
                raise ValueError("Record file is not available.")
            file_path = os.path.join(download_folder, record.record_file)
            if not os.path.exists(file_path):
                file_path = self._download_file(download_folder)
            return file_path
        except Exception as e:
            raise e
        
    @classmethod
    def get_valid_combinations(
        cls,
        dataset_name: str = None,
        script_name: str = None,
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None
    ) -> List[dict]:
        try:
            valid_combinations = ValidScriptDatasetCombinationsViewModel.search(
                dataset_name=dataset_name,
                script_name=script_name,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name
            )
            valid_combinations = [record.to_dict() for record in valid_combinations]
            return valid_combinations if valid_combinations else None
        except Exception as e:
            raise e
        

    @classmethod
    def _verify_records(cls, records: List["ScriptRecord"]) -> List["ScriptRecord"]:
        try:

            # Refresh all the views
            ExperimentScriptsViewModel.refresh()
            ExperimentDatasetsViewModel.refresh()
            ExperimentSeasonsViewModel.refresh()
            ExperimentSitesViewModel.refresh()

            # Verify the records
            script = None
            datasets = {}
            experiments = {}
            seasons = {}
            sites = {}

            # Get all the records
            for record in records:
                if not record.timestamp:
                    raise ValueError("Timestamp is required.")
                if not record.collection_date:
                    record.collection_date = record.timestamp.date()

                if script and record.script_name != script.script_name:
                    raise ValueError("All records must have the same script name.")
                
                if not script and ScriptModel.exists(script_name=record.script_name):
                    script = ScriptModel.get_by_parameters(script_name=record.script_name)

                record.script_id = script.id

                if record.dataset_name not in datasets: 
                    if DatasetModel.exists(dataset_name=record.dataset_name):
                        datasets[record.dataset_name] = DatasetModel.get_by_parameters(dataset_name=record.dataset_name)
                    else:
                        created_dataset = Dataset.create(
                            dataset_name=record.dataset_name,
                            experiment_name=record.experiment_name,
                            dataset_type=GEMINIDatasetType.Script
                        )
                        ExperimentDatasetsViewModel.refresh()
                        datasets[record.dataset_name] = DatasetModel.get_by_parameters(dataset_name=created_dataset.dataset_name)

                record.dataset_id = datasets[record.dataset_name].id

                if record.experiment_name not in experiments and ExperimentDatasetsViewModel.exists(experiment_name=record.experiment_name, dataset_name=record.dataset_name):
                    experiments[record.experiment_name] = ExperimentDatasetsViewModel.get_by_parameters(experiment_name=record.experiment_name, dataset_name=record.dataset_name)

                record.experiment_id = experiments[record.experiment_name].experiment_id

                if record.season_name not in seasons and ExperimentSeasonsViewModel.exists(experiment_name=record.experiment_name, season_name=record.season_name):
                    seasons[record.season_name] = ExperimentSeasonsViewModel.get_by_parameters(experiment_name=record.experiment_name, season_name=record.season_name)

                record.season_id = seasons[record.season_name].season_id

                if record.site_name not in sites and ExperimentSitesViewModel.exists(experiment_name=record.experiment_name, site_name=record.site_name):
                    sites[record.site_name] = ExperimentSitesViewModel.get_by_parameters(experiment_name=record.experiment_name, site_name=record.site_name)

                record.site_id = sites[record.site_name].site_id

            return records
        except Exception as e:
            raise e

        
    @classmethod
    def _preprocess_record(cls, record: 'ScriptRecord') -> 'ScriptRecord':
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
                    data_stream=file,
                    bucket_name="gemini"
                )
                return uploaded_file_url
        except Exception as e: 
            raise e
        

    def _download_file(self, output_folder: str) -> str:
        try:
            if not self.id:
                raise ValueError("Record ID is required to download the file.")
            record = ScriptRecordModel.get(self.id)
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
    def _create_file_uri(cls, record: 'ScriptRecord') -> str:
        try:
            file_path = record.record_file
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File {file_path} does not exist.")
            collection_date = record.collection_date.strftime("%Y-%m-%d")
            script_name = record.script_name
            experiment_name = record.experiment_name
            season_name = record.season_name
            site_name = record.site_name
            file_extension = os.path.splitext(file_path)[1]
            file_timestamp = str(int(record.timestamp.timestamp()*1000))
            file_key = f"script_data/{experiment_name}/{script_name}/{collection_date}/{site_name}/{season_name}/{file_timestamp}{file_extension}"
            return file_key
        except Exception as e:
            raise e
        


   

