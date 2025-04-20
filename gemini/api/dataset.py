from typing import Optional, List
from uuid import UUID
from tqdm import tqdm

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.enums import GEMINIDatasetType
from gemini.api.dataset_type import DatasetType
from gemini.api.dataset_record import DatasetRecord
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.dataset_types import DatasetTypeModel
from gemini.db.models.associations import ExperimentDatasetModel
from gemini.db.models.views.experiment_views import ExperimentDatasetsViewModel

from datetime import date, datetime

class Dataset(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "dataset_id"))

    collection_date: date
    dataset_name: str
    dataset_info: Optional[dict] = None
    dataset_type_id: int

    @classmethod
    def exists(
        cls,
        dataset_name: str
    ) -> bool:
        try:
            exists = DatasetModel.exists(dataset_name=dataset_name)
            return exists
        except Exception as e:
            raise e

    @classmethod
    def create(
        cls,
        dataset_name: str,
        dataset_info: dict = {},
        dataset_type: GEMINIDatasetType = GEMINIDatasetType.Default,
        collection_date: date = date.today(),
        experiment_name: str = None
    ) -> "Dataset":
        try:

            dataset_type_id = dataset_type.value
            db_instance = DatasetModel.get_or_create(
                collection_date=collection_date,
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                dataset_type_id=dataset_type_id,
            )
            dataset = cls.model_validate(db_instance)
            if experiment_name:
                dataset.assign_experiment(experiment_name=experiment_name)
            return dataset
        except Exception as e:
            raise e
        
    @classmethod
    def get(cls, dataset_name: str, experiment_name: str = None) -> "Dataset":
        try:
            db_instance = ExperimentDatasetsViewModel.get_by_parameters(
                dataset_name=dataset_name,
                experiment_name=experiment_name
            )
            dataset = cls.model_validate(db_instance) if db_instance else None
            return dataset
        except Exception as e:
            raise e
        
    def get_info(self) -> dict:
        try:
            current_id = self.id
            dataset = DatasetModel.get(current_id)
            dataset_info = dataset.dataset_info
            if not dataset_info:
                raise Exception("Dataset info is empty.")
            return dataset_info
        except Exception as e:
            raise e
        
    def set_info(self, dataset_info: dict) -> "Dataset":
        try:
            current_id = self.id
            dataset = DatasetModel.get(current_id)
            dataset = DatasetModel.update(
                dataset,
                dataset_info=dataset_info,
            )
            dataset = self.model_validate(dataset)
            self.refresh()
            return dataset
        except Exception as e:
            raise e

  
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Dataset":
        try:
            db_instance = DatasetModel.get(id)
            dataset = cls.model_validate(db_instance) if db_instance else None
            return dataset
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["Dataset"]:
        try:
            datasets = DatasetModel.all()
            datasets = [cls.model_validate(dataset) for dataset in datasets]
            return datasets if datasets else None
        except Exception as e:
            raise e
        

    @classmethod
    def search(
        cls, 
        experiment_name: str = None,
        dataset_name: str = None,
        dataset_info: dict = None,
        dataset_type: GEMINIDatasetType = None,
        collection_date: date = None,
    ) -> List["Dataset"]:
        try:
            if not experiment_name and not dataset_name and not dataset_info and not dataset_type and not collection_date:
                raise ValueError("At least one parameter must be provided.")

            datasets = ExperimentDatasetsViewModel.search(
                experiment_name=experiment_name,
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                dataset_type=dataset_type,
                collection_date=collection_date,
            )
            datasets = [cls.model_validate(dataset) for dataset in datasets]
            return datasets if datasets else None
        except Exception as e:
            raise e
        
    def update(
            self,
            dataset_name: str = None,
            dataset_info: dict = None,
            dataset_type: GEMINIDatasetType = None,
            collection_date: date = None 
    ) -> "Dataset":
        try:
            if not dataset_name and not dataset_info and not dataset_type and not collection_date:
                raise ValueError("At least one parameter must be provided.")

            current_id = self.id
            dataset = DatasetModel.get(current_id)
            dataset = DatasetModel.update(
                dataset,
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                dataset_type_id=dataset_type.value if dataset_type else None,
                collection_date=collection_date
            )
            dataset = self.model_validate(dataset)
            self.refresh()
            return dataset
        except Exception as e:
            raise e
        
    def delete(self) ->  bool:
        try:
            current_id = self.id
            dataset = DatasetModel.get(current_id)
            DatasetModel.delete(dataset)
            return True
        except Exception as e:
            raise e
        
    def refresh(self) -> "Dataset":
        try:
            db_instance = DatasetModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e
        
    def get_type(self) -> DatasetType:
        try:
            dataset = DatasetModel.get(self.id)
            dataset_type = DatasetTypeModel.get(dataset.dataset_type_id)
            dataset_type = DatasetType.model_validate(dataset_type)
            return dataset_type if dataset_type else None
        except Exception as e:
            raise e


    def get_experiments(self):
        try:
            from gemini.api.experiment import Experiment
            db_instance = DatasetModel.get(self.id)
            experiments = ExperimentDatasetsViewModel.search(dataset_id=db_instance.id)
            experiments = [Experiment.model_validate(experiment) for experiment in experiments]
            return experiments if experiments else None
        except Exception as e:
            raise e
        
    def assign_experiment(self, experiment_name: str) -> bool:
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name)
            if not experiment:
                raise Exception(f"Experiment {experiment_name} does not exist.")
            if experiment.has_dataset(self.dataset_name):
                print(f"Dataset {self.dataset_name} already exists in experiment {experiment_name}.")
                return True
            ExperimentDatasetModel.get_or_create(experiment_id=experiment.id, dataset_id=self.id)
            return True
        except Exception as e:
            return False
        
    def belongs_to_experiment(self, experiment_name: str) -> bool:
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name)
            if not experiment:
                raise Exception(f"Experiment {experiment_name} does not exist.")
            belongs = experiment.has_dataset(self.dataset_name)
            return belongs
        except Exception as e:
            return False
        
    def unassign_experiment(self, experiment_name: str) -> bool:
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name)
            if not experiment:
                raise Exception(f"Experiment {experiment_name} does not exist.")
            if not experiment.has_dataset(self.dataset_name):
                print(f"Dataset {self.dataset_name} does not exist in experiment {experiment_name}.")
                return False
            experiment_dataset_instance = ExperimentDatasetModel.get_by_parameters(
                experiment_id=experiment.id,
                dataset_id=self.id
            )
            if not experiment_dataset_instance:
                raise Exception(f"ExperimentDataset instance not found for dataset {self.dataset_name} in experiment {experiment_name}.")
            is_deleted = ExperimentDatasetModel.delete(experiment_dataset_instance)
            return is_deleted
        except Exception as e:
            return False

    def add_record(
        self,
        timestamp: datetime = None,
        collection_date: date = None,
        dataset_data: dict = {},
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        record_file: str = None,
        record_info: dict = {} 
    ) -> tuple[bool, List[str]]:
        try:

            if not experiment_name and not season_name and not site_name:
                raise ValueError("Please provide at least one of the following: experiment_name, season_name, site_name.")

            timestamp = timestamp if timestamp else datetime.now()
            collection_date = collection_date if collection_date else timestamp.date()
            dataset_name = self.dataset_name
            dataset_id = self.id

            dataset_record = DatasetRecord(
                timestamp=timestamp,
                collection_date=collection_date,
                dataset_id=dataset_id,
                dataset_name=dataset_name,
                dataset_data=dataset_data,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                record_file=record_file if record_file else None,
                record_info=record_info if record_info else {}
            )
            success, inserted_record_ids = DatasetRecord.add([dataset_record])
            return success, inserted_record_ids
        except Exception as e:
            return False, []
        
    def add_records(
        self,
        timestamps: List[datetime] = None,
        collection_date: date = None,
        dataset_data: List[dict] = [],
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        record_files: List[str] = None,
        record_info: List[dict] = []
    ) -> tuple[bool, List[str]]:
        try:
            if not experiment_name and not season_name and not site_name:
                raise ValueError("Please provide at least one of the following: experiment_name, season_name, site_name.")
            
            if len(timestamps) == 0:
                raise ValueError("Please provide at least one timestamp.")
            
            collection_date = collection_date if collection_date else timestamps[0].date()
            dataset_records = []
            timestamps_length = len(timestamps)

            for i in tqdm(range(timestamps_length), desc="Arranging Records for Sensor: " + self.dataset_name):
                dataset_record = DatasetRecord(
                    timestamp=timestamps[i],
                    collection_date=collection_date,
                    dataset_id=self.id,
                    dataset_name=self.dataset_name,
                    dataset_data=dataset_data[i] if dataset_data else {},
                    experiment_name=experiment_name,
                    season_name=season_name,
                    site_name=site_name,
                    record_file=record_files[i] if record_files else None,
                    record_info=record_info[i] if record_info else {}
                )
                dataset_records.append(dataset_record)
            success, inserted_record_ids = DatasetRecord.add(dataset_records)
            return success, inserted_record_ids
        except Exception as e:
            return False, []
        
    def get_records(
        self,
        collection_date: date = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        record_info: dict = None,
    ) -> List[DatasetRecord]:
        try:
            record_info = record_info if record_info else {}
            record_info = {k: v for k, v in record_info.items() if v is not None}

            records = DatasetRecord.search(
                collection_date=collection_date,
                dataset_name=self.dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                record_info=record_info
            )
            return records
        except Exception as e:
            raise e
