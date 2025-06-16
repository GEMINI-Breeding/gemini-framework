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

    def __str__(self):
        return f"Dataset(name={self.dataset_name}, collection_date={self.collection_date}, dataset_type={GEMINIDatasetType(self.dataset_type_id).name}, id={self.id})"
    
    def __repr__(self):
        return f"Dataset(dataset_name={self.dataset_name}, collection_date={self.collection_date}, dataset_type={GEMINIDatasetType(self.dataset_type_id).name}, id={self.id})"
    
    @classmethod
    def exists(
        cls,
        dataset_name: str,
    ) -> bool:
        try:
            exists = DatasetModel.exists(
                dataset_name=dataset_name,
            )
            return exists
        except Exception as e:
            print(f"Error checking existence of dataset: {e}")
            return False
        
    @classmethod
    def create(
        cls,
        dataset_name: str,
        dataset_info: dict = {},
        dataset_type: GEMINIDatasetType = GEMINIDatasetType.Default,
        collection_date: date = date.today(),
        experiment_name: str = None
    ) -> Optional["Dataset"]:
        try:
            db_instance = DatasetModel.get_or_create(
                collection_date=collection_date,
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                dataset_type_id=dataset_type.value,
            )
            dataset = cls.model_validate(db_instance)
            if experiment_name:
                dataset.associate_experiment(experiment_name=experiment_name)
            return dataset
        except Exception as e:
            print(f"Error creating dataset: {e}")
            return None
        
    @classmethod
    def get(
        cls,
        dataset_name: str,
        experiment_name: str = None
    ) -> Optional["Dataset"]:
        try:
            db_instance = ExperimentDatasetsViewModel.get_by_parameters(
                dataset_name=dataset_name,
                experiment_name=experiment_name
            )
            if not db_instance:
                print(f"Dataset with name {dataset_name} not found.")
                return None
            dataset = cls.model_validate(db_instance)
            return dataset
        except Exception as e:
            print(f"Error getting dataset: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["Dataset"]:
        try:
            db_instance = DatasetModel.get(id)
            if not db_instance:
                print(f"Dataset with ID {id} does not exist.")
                return None
            dataset = cls.model_validate(db_instance)
            return dataset
        except Exception as e:
            print(f"Error getting dataset by ID: {e}")
            return None
        
    @classmethod
    def get_all(cls) -> Optional[List["Dataset"]]:
        try:
            datasets = DatasetModel.all()
            if not datasets or len(datasets) == 0:
                print("No datasets found.")
                return None
            datasets = [cls.model_validate(dataset) for dataset in datasets]
            return datasets
        except Exception as e:
            print(f"Error getting all datasets: {e}")
            return None
        
    @classmethod
    def search(
        cls,
        dataset_name: str = None,
        dataset_info: dict = None,
        dataset_type: GEMINIDatasetType = None,
        collection_date: date = None,
        experiment_name: str = None,
    ) -> Optional[List["Dataset"]]:
        try:
            if not any([dataset_name, dataset_info, dataset_type, collection_date, experiment_name]):
                print("At least one parameter must be provided.")
                return None
            datasets = ExperimentDatasetsViewModel.search(
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                dataset_type=dataset_type,
                collection_date=collection_date,
                experiment_name=experiment_name
            )
            if not datasets or len(datasets) == 0:
                print("No datasets found with the provided search parameters.")
                return None
            datasets = [cls.model_validate(dataset) for dataset in datasets]
            return datasets
        except Exception as e:
            print(f"Error searching datasets: {e}")
            return None
        
    def update(
        self,
        dataset_name: str = None,
        dataset_info: dict = None,
        dataset_type: GEMINIDatasetType = None,
        collection_date: date = None
    ) -> Optional["Dataset"]:
        try:
            if not any([dataset_name, dataset_info, dataset_type, collection_date]):
                print("At least one parameter must be provided for update.")
                return None
            current_id = self.id
            dataset = DatasetModel.get(current_id)
            if not dataset:
                print(f"Dataset with ID {current_id} does not exist.")
                return None
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
            print(f"Error updating dataset: {e}")
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            dataset = DatasetModel.get(current_id)
            if not dataset:
                print(f"Dataset with ID {current_id} does not exist.")
                return False
            DatasetModel.delete(dataset)
            return True
        except Exception as e:
            print(f"Error deleting dataset: {e}")
            return False
        
    def refresh(self) -> Optional["Dataset"]:
        try:
            db_instance = DatasetModel.get(self.id)
            if not db_instance:
                print(f"Dataset with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing dataset: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            dataset = DatasetModel.get(current_id)
            if not dataset:
                print(f"Dataset with ID {current_id} does not exist.")
                return None
            dataset_info = dataset.dataset_info
            if not dataset_info:
                print("Dataset info is empty.")
                return None
            return dataset_info
        except Exception as e:
            print(f"Error getting dataset info: {e}")
            return None
        
    def set_info(self, dataset_info: dict) -> Optional["Dataset"]:
        try:
            current_id = self.id
            dataset = DatasetModel.get(current_id)
            if not dataset:
                print(f"Dataset with ID {current_id} does not exist.")
                return None
            dataset = DatasetModel.update(
                dataset,
                dataset_info=dataset_info,
            )
            dataset = self.model_validate(dataset)
            self.refresh()
            return dataset
        except Exception as e:
            print(f"Error setting dataset info: {e}")
            return None
        
    def get_associated_experiments(self):
        try:
            from gemini.api.experiment import Experiment
            current_id = self.id
            experiment_datasets = ExperimentDatasetsViewModel.search(dataset_id=current_id)
            if not experiment_datasets or len(experiment_datasets) == 0:
                print(f"No experiments associated with dataset ID {current_id}.")
                return None
            experiments = [Experiment.model_validate(experiment) for experiment in experiment_datasets]
            return experiments
        except Exception as e:
            print(f"Error getting associated experiments: {e}")
            return None

    def associate_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return None
            existing_association = ExperimentDatasetModel.get_by_parameters(
                experiment_id=experiment.id,
                dataset_id=self.id
            )
            if existing_association:
                print(f"Dataset {self.dataset_name} is already associated with experiment {experiment_name}.")
                return experiment
            association = ExperimentDatasetModel.get_or_create(
                experiment_id=experiment.id,
                dataset_id=self.id
            )
            if not association:
                print(f"Failed to associate dataset {self.dataset_name} with experiment {experiment_name}.")
                return None
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error associating dataset with experiment: {e}")
            return None 

    def unassociate_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return None
            existing_association = ExperimentDatasetModel.get_by_parameters(
                experiment_id=experiment.id,
                dataset_id=self.id
            )
            if not existing_association:
                print(f"Dataset {self.dataset_name} is not associated with experiment {experiment_name}.")
                return None
            is_deleted = ExperimentDatasetModel.delete(existing_association)
            if not is_deleted:
                print(f"Failed to unassociate dataset {self.dataset_name} from experiment {experiment_name}.")
                return None
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error unassociating dataset from experiment: {e}")
            return None

    def belongs_to_experiment(self, experiment_name: str) -> bool:
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return False
            association_exists = ExperimentDatasetModel.exists(
                experiment_id=experiment.id,
                dataset_id=self.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking if dataset belongs to experiment: {e}")
            return False
        

    def insert_record(
        self,
        timestamp: datetime = None,
        collection_date: date = None,
        dataset_data: dict = {},
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        record_file: str = None,
        record_info: dict = {},
    ) -> tuple[bool, List[str]]:
        try:
            if not experiment_name and not season_name and not site_name:
                raise ValueError("Please provide at least one of the following: experiment_name, season_name, site_name.")

            if not dataset_data and not record_file:
                raise ValueError("Please provide either dataset_data or record_file.")
            
            timestamp = timestamp if timestamp else datetime.now()
            collection_date = collection_date if collection_date else timestamp.date()
            dataset_name = self.dataset_name
            dataset_record = DatasetRecord.create(
                timestamp=timestamp,
                collection_date=collection_date,
                dataset_name=dataset_name,
                dataset_data=dataset_data,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                record_file=record_file if record_file else None,
                record_info=record_info if record_info else {},
                insert_on_create=False
            )
            success, inserted_record_ids = DatasetRecord.insert([dataset_record])
            if not success:
                print(f"Failed to add record for dataset {self.dataset_name}.")
            return success, inserted_record_ids
        except Exception as e:
            print(f"Error adding record to dataset {self.dataset_name}: {e}")
            return False, []
        
    def insert_records(
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
            
            if len(dataset_data) != len(timestamps):
                raise ValueError("dataset_data length must match timestamps length.")
            
            if record_files and len(record_files) != len(timestamps):
                raise ValueError("record_files length must match timestamps length.")
            
            collection_date = collection_date if collection_date else timestamps[0].date()
            dataset_records = []
            timestamps_length = len(timestamps)

            for i in tqdm(range(timestamps_length), desc="Arranging Records for Dataset: " + self.dataset_name):
                dataset_record = DatasetRecord.create(
                    timestamp=timestamps[i],
                    collection_date=collection_date,
                    dataset_name=self.dataset_name,
                    dataset_data=dataset_data[i] if dataset_data else {},
                    experiment_name=experiment_name,
                    season_name=season_name,
                    site_name=site_name,
                    record_file=record_files[i] if record_files else None,
                    record_info=record_info[i] if record_info else {},
                    insert_on_create=False
                )
                dataset_records.append(dataset_record)
            success, inserted_record_ids = DatasetRecord.insert(dataset_records)
            if not success:
                print(f"Failed to add records for dataset {self.dataset_name}.")
                return False, []
            return success, inserted_record_ids
        except Exception as e:
            print(f"Error adding records to dataset {self.dataset_name}: {e}")
            return False, []
        
    def search_records(
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
            print(f"Error searching records in dataset {self.dataset_name}: {e}")
            return []
        

    def filter_records(
        self,
        start_timestamp: Optional[datetime] = None,
        end_timestamp: Optional[datetime] = None,
        experiment_names: Optional[List[str]] = None,
        season_names: Optional[List[str]] = None,
        site_names: Optional[List[str]] = None
    ) -> List[DatasetRecord]:
        try:
            records = DatasetRecord.filter(
                dataset_names=[self.dataset_name],
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
                experiment_names=experiment_names,
                season_names=season_names,
                site_names=site_names
            )
            return records
        except Exception as e:
            print(f"Error filtering records in dataset {self.dataset_name}: {e}")
            return []
            