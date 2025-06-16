from typing import Optional, List
from uuid import UUID
from tqdm import tqdm

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.dataset import Dataset, GEMINIDatasetType
from gemini.api.model_run import ModelRun
from gemini.api.model_record import ModelRecord
from gemini.db.models.models import ModelModel
from gemini.db.models.model_runs import ModelRunModel
from gemini.db.models.associations import ExperimentModelModel, ModelDatasetModel
from gemini.db.models.views.experiment_views import ExperimentModelsViewModel
from gemini.db.models.views.dataset_views import ModelDatasetsViewModel
from gemini.db.models.views.run_views import ModelRunsViewModel

from datetime import date, datetime

class Model(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "model_id"))

    model_name: str
    model_url: Optional[str] = None
    model_info: Optional[dict] = None

    def __str__(self):
        return f"Model(name={self.model_name}, url={self.model_url}, id={self.id})"
    
    def __repr__(self):
        return f"Model(model_name={self.model_name}, model_url={self.model_url}, id={self.id})"
    
    @classmethod
    def exists(
        cls,
        model_name: str
    ) -> bool:
        try:
            exists = ModelModel.exists(model_name=model_name)
            return exists
        except Exception as e:
            print(f"Error checking existence of model: {e}")
            return False
        
    @classmethod
    def create(
        cls,
        model_name: str,
        model_url: str = None,
        model_info: dict = {},
        experiment_name: str = None
    ) -> Optional["Model"]:
        try:
            db_instance = ModelModel.get_or_create(
                model_name=model_name,
                model_url=model_url,
                model_info=model_info,
            )
            model = cls.model_validate(db_instance)
            if experiment_name:
                model.associate_experiment(experiment_name=experiment_name)
            return model
        except Exception as e:
            print(f"Error creating model: {e}")
            return None
        
    @classmethod
    def get(
        cls,
        model_name: str,
        experiment_name: str = None
    ) -> Optional["Model"]:
        try:
            db_instance = ExperimentModelsViewModel.get_by_parameters(
                model_name=model_name,
                experiment_name=experiment_name
            )
            if not db_instance:
                print(f"Model with name {model_name} not found.")
                return None
            model = cls.model_validate(db_instance)
            return model
        except Exception as e:
            print(f"Error getting model: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["Model"]:
        try:
            db_instance = ModelModel.get(id)
            if not db_instance:
                print(f"Model with ID {id} does not exist.")
                return None
            model = cls.model_validate(db_instance)
            return model
        except Exception as e:
            print(f"Error getting model by ID: {e}")
            return None
        
    @classmethod
    def get_all(cls) -> Optional[List["Model"]]:
        try:
            models = ModelModel.all()
            if not models or len(models) == 0:
                print("No models found.")
                return None
            models = [cls.model_validate(model) for model in models]
            return models
        except Exception as e:
            print(f"Error getting all models: {e}")
            return None
        
    @classmethod
    def search(
        cls,
        model_name: str = None,
        model_info: dict = None,
        model_url: str = None,
        experiment_name: str = None
    ) -> Optional[List["Model"]]:
        try:
            if not any([model_name, model_info, model_url, experiment_name]):
                print("At least one search parameter must be provided.")
                return None
            models = ExperimentModelsViewModel.search(
                model_name=model_name,
                model_info=model_info,
                model_url=model_url,
                experiment_name=experiment_name
            )
            if not models or len(models) == 0:
                print("No models found with the provided search parameters.")
                return None
            models = [cls.model_validate(model) for model in models]
            return models
        except Exception as e:
            print(f"Error searching models: {e}")
            return None
        
    def update(
        self,
        model_name: str = None,
        model_url: str = None,
        model_info: dict = None
    ) -> Optional["Model"]:
        try:
            if not any([model_name, model_url, model_info]):
                print("At least one update parameter must be provided.")
                return None
            current_id = self.id
            model = ModelModel.get(current_id)
            if not model:
                print(f"Model with ID {current_id} does not exist.")
                return None
            model = ModelModel.update(
                model,
                model_name=model_name,
                model_url=model_url,
                model_info=model_info
            )
            model = self.model_validate(model)
            self.refresh()
            return model
        except Exception as e:
            print(f"Error updating model: {e}")
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            model = ModelModel.get(current_id)
            if not model:
                print(f"Model with ID {current_id} does not exist.")
                return False
            ModelModel.delete(model)
            return True
        except Exception as e:
            print(f"Error deleting model: {e}")
            return False
        
    def refresh(self) -> Optional["Model"]:
        try:
            db_instance = ModelModel.get(self.id)
            if not db_instance:
                print(f"Model with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing model: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            model = ModelModel.get(current_id)
            if not model:
                print(f"Model with ID {current_id} does not exist.")
                return None
            model_info = model.model_info
            if not model_info:
                print("Model info is empty.")
                return None
            return model_info
        except Exception as e:
            print(f"Error getting model info: {e}")
            return None
        
    def set_info(self, model_info: dict) -> Optional["Model"]:
        try:
            current_id = self.id
            model = ModelModel.get(current_id)
            if not model:
                print(f"Model with ID {current_id} does not exist.")
                return None
            model = ModelModel.update(
                model,
                model_info=model_info
            )
            model = self.model_validate(model)
            self.refresh()
            return model
        except Exception as e:
            print(f"Error setting model info: {e}")
            return None
        
    def get_associated_runs(self):
        try:
            from gemini.api.model_run import ModelRun
            current_id = self.id
            model_runs = ModelRunsViewModel.search(model_id=current_id)
            if not model_runs or len(model_runs) == 0:
                print(f"No runs associated with model {self.model_name}.")
                return None
            runs = [ModelRun.model_validate(model_run) for model_run in model_runs]
            return runs
        except Exception as e:
            print(f"Error getting associated runs: {e}")
            return None

    def create_new_run(self, model_run_info: dict):
        try:
            from gemini.api.model_run import ModelRun
            current_name = self.model_name
            model_run = ModelRun.create(
                model_run_info=model_run_info,
                model_name=current_name
            )
            if not model_run:
                print(f"Failed to create run for model {self.model_name}.")
                return None
            return model_run
        except Exception as e:
            print(f"Error creating run: {e}")
            return None

    def get_associated_experiments(self):
        try:
            from gemini.api.experiment import Experiment
            current_id = self.id
            experiment_models = ExperimentModelsViewModel.search(model_id=current_id)
            if not experiment_models or len(experiment_models) == 0:
                print(f"No experiments associated with model {self.model_name}.")
                return None
            experiments = [Experiment.model_validate(experiment) for experiment in experiment_models]
            return experiments
        except Exception as e:
            print(f"Error getting associated experiments: {e}")
            return None

    def associate_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return None
            existing_association = ExperimentModelModel.exists(
                experiment_id=experiment.id,
                model_id=self.id
            )
            if existing_association:
                print(f"Model {self.model_name} is already associated with experiment {experiment_name}.")
                return experiment
            new_association = ExperimentModelModel.get_or_create(
                experiment_id=experiment.id,
                model_id=self.id
            )
            if not new_association:
                print(f"Failed to associate model {self.model_name} with experiment {experiment_name}.")
                return None
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error associating experiment: {e}")
            return None

    def unassociate_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return None
            existing_association = ExperimentModelModel.get_by_parameters(
                experiment_id=experiment.id,
                model_id=self.id
            )
            if not existing_association:
                print(f"Model {self.model_name} is not associated with experiment {experiment_name}.")
                return None
            is_deleted = ExperimentModelModel.delete(existing_association)
            if not is_deleted:
                print(f"Failed to disassociate model {self.model_name} from experiment {experiment_name}.")
                return None
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error disassociating experiment: {e}")
            return None

    def belongs_to_experiment(self, experiment_name: str) -> bool:
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return False
            association_exists = ExperimentModelModel.exists(
                experiment_id=experiment.id,
                model_id=self.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking experiment membership: {e}")
            return False
        
    def get_associated_datasets(self):
        try:
            from gemini.api.dataset import Dataset
            current_id = self.id
            model_datasets = ModelDatasetsViewModel.search(model_id=current_id)
            if not model_datasets or len(model_datasets) == 0:
                print(f"No datasets associated with model {self.model_name}.")
                return None
            datasets = [Dataset.model_validate(model_dataset) for model_dataset in model_datasets]
            return datasets
        except Exception as e:
            print(f"Error getting associated datasets: {e}")
            return None

    def create_new_dataset(
        self,
        dataset_name: str,
        dataset_info: dict = {},
        collection_date: date = None,
        experiment_name: str = None
    ):
        try:
            from gemini.api.dataset import Dataset
            dataset = Dataset.create(
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                collection_date=collection_date,
                experiment_name=experiment_name,
                dataset_type=GEMINIDatasetType.Model
            )
            if not dataset:
                print(f"Failed to create dataset for model {self.model_name}.")
                return None
            dataset = self.associate_dataset(dataset_name=dataset_name)
            return dataset
        except Exception as e:
            print(f"Error creating dataset: {e}")
            return None
        
    def associate_dataset(self, dataset_name: str):
        try:
            from gemini.api.dataset import Dataset
            dataset = Dataset.get(dataset_name=dataset_name)
            if not dataset:
                print(f"Dataset {dataset_name} does not exist.")
                return None
            existing_association = ModelDatasetModel.exists(
                dataset_id=dataset.id,
                model_id=self.id
            )
            if existing_association:
                print(f"Model {self.model_name} is already associated with dataset {dataset_name}.")
                return dataset
            new_association = ModelDatasetModel.get_or_create(
                dataset_id=dataset.id,
                model_id=self.id
            )
            if not new_association:
                print(f"Failed to associate model {self.model_name} with dataset {dataset_name}.")
                return None
            self.refresh()
            return dataset
        except Exception as e:
            print(f"Error associating dataset: {e}")
            return None
        

    def insert_record(
        self,
        timestamp: datetime = None,
        collection_date: date = None,
        model_data: dict = {},
        dataset_name: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        record_file: str = None,
        record_info: dict = {},
    ) -> tuple[bool, List[str]]:
        try:
            if not experiment_name and not season_name and not site_name:
                raise ValueError("At least one of experiment_name, season_name, or site_name must be provided.")
            
            if not model_data and not record_file:
                raise ValueError("Either model_data or record_file must be provided.")
            
            timestamp = timestamp if timestamp else datetime.now()
            collection_date = collection_date if collection_date else timestamp.date()
            if not dataset_name:
                dataset_name = f"{self.model_name} Dataset {collection_date}"
            model_name = self.model_name
            model_record = ModelRecord.create(
                timestamp=timestamp,
                collection_date=collection_date,
                model_name=model_name,
                model_data=model_data,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                record_file=record_file,
                record_info=record_info,
                insert_on_create=False
            )
            success, inserted_record_ids = ModelRecord.insert([model_record])
            if not success:
                raise Exception("Failed to insert model record.")
            return success, inserted_record_ids
        except Exception as e:
            print(f"Error inserting model record: {e}")
            return False, []
        
    def insert_records(
        self,
        timestamps: List[datetime] = None,
        collection_date: date = None,
        model_data: List[dict] = [],
        dataset_name: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        record_files: List[str] = [],
        record_info: List[dict] = []
    ) -> tuple[bool, List[str]]:
        try:
            if not experiment_name and not season_name and not site_name:
                raise ValueError("At least one of experiment_name, season_name, or site_name must be provided.")
            
            if len(timestamps) == 0:
                raise ValueError("At least one timestamp must be provided.")
            
            if len(model_data) != len(timestamps):
                raise ValueError("model_data must have the same length as timestamps.")
            
            if record_files and len(record_files) != len(timestamps):
                raise ValueError("record_files must have the same length as timestamps.")
            
            collection_date = collection_date if collection_date else timestamps[0].date()
            
            if not dataset_name:
                dataset_name = f"{self.model_name} Dataset {collection_date}"
            
            model_records = []
            timestamps_length = len(timestamps)

            for i in tqdm(range(timestamps_length), desc="Arranging Records for Model " + self.model_name):
                model_record = ModelRecord.create(
                    timestamp = timestamps[i],
                    collection_date = collection_date,
                    model_name= self.model_name,
                    model_data = model_data[i]  if model_data else {},
                    dataset_name = dataset_name,
                    experiment_name = experiment_name,
                    season_name = season_name,
                    site_name = site_name,
                    record_file= record_files[i] if record_files else None,
                    record_info = record_info[i] if record_info else {},
                    insert_on_create=False
                )
                model_records.append(model_record)

            success, inserted_record_ids = ModelRecord.insert(model_records)
            if not success:
                print("Failed to insert model records.")
                return False, []
            return success, inserted_record_ids
        except Exception as e:
            print(f"Error inserting model records: {e}")
            return False, []
        
    def search_records(
        self,
        collection_date: date = None,
        dataset_name: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        record_info: dict = None
    ) -> List[ModelRecord]:
        try:
            record_info = record_info if record_info else {}
            record_info = {k: v for k, v in record_info.items() if v is not None}

            records = ModelRecord.search(
                collection_date=collection_date,
                dataset_name=dataset_name,
                model_name=self.model_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                record_info=record_info
            )
            return records
        except Exception as e:
            print(f"Error searching model records: {e}")
            return []
        
    def filter_records(
        self,
        start_timestamp: Optional[datetime] = None,
        end_timestamp: Optional[datetime] = None,
        dataset_names: Optional[List[str]] = None,
        experiment_names: Optional[List[str]] = None,
        season_names: Optional[List[str]] = None,
        site_names: Optional[List[str]] = None
    ) -> List[ModelRecord]:
        try:
            records = ModelRecord.filter(
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
                model_names=[self.model_name],
                dataset_names=dataset_names,
                experiment_names=experiment_names,
                season_names=season_names,
                site_names=site_names
            )
            return records
        except Exception as e:
            print(f"Error filtering model records: {e}")
            return []
        
