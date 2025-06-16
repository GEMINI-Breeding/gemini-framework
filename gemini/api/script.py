from typing import Optional, List
from uuid import UUID
from tqdm import tqdm

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.script_run import ScriptRun
from gemini.api.script_record import ScriptRecord
from gemini.api.dataset import Dataset, GEMINIDatasetType
from gemini.db.models.scripts import ScriptModel
from gemini.db.models.script_runs import ScriptRunModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.associations import ExperimentScriptModel, ScriptDatasetModel
from gemini.db.models.views.experiment_views import ExperimentScriptsViewModel
from gemini.db.models.views.dataset_views import ScriptDatasetsViewModel
from gemini.db.models.views.run_views import ScriptRunsViewModel
from datetime import date, datetime


class Script(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "script_id"))

    script_name: str
    script_url: Optional[str] = None
    script_extension: Optional[str] = None
    script_info: Optional[dict] = None

    def __str__(self):
        return f"Script(name={self.script_name}, url={self.script_url}, extension={self.script_extension}, id={self.id})"
    
    def __repr__(self):
        return f"Script(script_name={self.script_name}, script_url={self.script_url}, script_extension={self.script_extension}, id={self.id})"

    @classmethod
    def exists(
        cls,
        script_name: str
    ) -> bool:
        try:
            exists = ScriptModel.exists(script_name=script_name)
            return exists
        except Exception as e:
            print(f"Error checking existence of script: {e}")
            return False

    @classmethod
    def create(
        cls,
        script_name: str,
        script_url: str = None,
        script_extension: str = None,
        script_info: dict = {},
        experiment_name: str = None
    ) -> Optional["Script"]:
        try:
            db_instance = ScriptModel.get_or_create(
                script_name=script_name,
                script_url=script_url,
                script_extension=script_extension,
                script_info=script_info,
            )
            script = cls.model_validate(db_instance)
            if experiment_name:
                script.associate_experiment(experiment_name=experiment_name)
            return script
        except Exception as e:
            print(f"Error creating script: {e}")
            return None

    @classmethod
    def get(
        cls,
        script_name: str,
        experiment_name: str = None
    ) -> Optional["Script"]:
        try:
            db_instance = ExperimentScriptsViewModel.get_by_parameters(
                script_name=script_name,
                experiment_name=experiment_name
            )
            if not db_instance:
                print(f"Script with name {script_name} not found.")
                return None
            script = cls.model_validate(db_instance)
            return script
        except Exception as e:
            print(f"Error getting script: {e}")
            return None

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["Script"]:
        try:
            db_instance = ScriptModel.get(id)
            if not db_instance:
                print(f"Script with ID {id} does not exist.")
                return None
            script = cls.model_validate(db_instance)
            return script
        except Exception as e:
            print(f"Error getting script by ID: {e}")
            return None

    @classmethod
    def get_all(cls) -> Optional[List["Script"]]:
        try:
            scripts = ScriptModel.all()
            if not scripts or len(scripts) == 0:
                print("No scripts found.")
                return None
            scripts = [cls.model_validate(script) for script in scripts]
            return scripts
        except Exception as e:
            print(f"Error getting all scripts: {e}")
            return None

    @classmethod
    def search(
        cls,
        script_name: str = None,
        script_info: dict = None,
        script_url: str = None,
        script_extension: str = None,
        experiment_name: str = None
    ) -> Optional[List["Script"]]:
        try:
            if not any([script_name, script_info, script_url, script_extension, experiment_name]):
                print("At least one search parameter must be provided.")
                return None
            scripts = ExperimentScriptsViewModel.search(
                script_name=script_name,
                script_info=script_info,
                script_url=script_url,
                script_extension=script_extension,
                experiment_name=experiment_name
            )
            if not scripts or len(scripts) == 0:
                print("No scripts found with the provided search parameters.")
                return None
            scripts = [cls.model_validate(script) for script in scripts]
            return scripts
        except Exception as e:
            print(f"Error searching scripts: {e}")
            return None

    def update(
        self,
        script_name: str = None,
        script_url: str = None,
        script_extension: str = None,
        script_info: dict = None
    ) -> Optional["Script"]:
        try:
            if not any([script_name, script_url, script_extension, script_info]):
                print("At least one update parameter must be provided.")
                return None
            current_id = self.id
            script = ScriptModel.get(current_id)
            if not script:
                print(f"Script with ID {current_id} does not exist.")
                return None
            script = ScriptModel.update(
                script,
                script_name=script_name,
                script_url=script_url,
                script_extension=script_extension,
                script_info=script_info
            )
            script = self.model_validate(script)
            self.refresh()
            return script
        except Exception as e:
            print(f"Error updating script: {e}")
            return None

    def delete(self) -> bool:
        try:
            current_id = self.id
            script = ScriptModel.get(current_id)
            if not script:
                print(f"Script with ID {current_id} does not exist.")
                return False
            ScriptModel.delete(script)
            return True
        except Exception as e:
            print(f"Error deleting script: {e}")
            return False

    def refresh(self) -> Optional["Script"]:
        try:
            db_instance = ScriptModel.get(self.id)
            if not db_instance:
                print(f"Script with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing script: {e}")
            return None

    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            script = ScriptModel.get(current_id)
            if not script:
                print(f"Script with ID {current_id} does not exist.")
                return None
            script_info = script.script_info
            if not script_info:
                print("Script info is empty.")
                return None
            return script_info
        except Exception as e:
            print(f"Error getting script info: {e}")
            return None

    def set_info(self, script_info: dict) -> Optional["Script"]:
        try:
            current_id = self.id
            script = ScriptModel.get(current_id)
            if not script:
                print(f"Script with ID {current_id} does not exist.")
                return None
            script = ScriptModel.update(
                script,
                script_info=script_info
            )
            script = self.model_validate(script)
            self.refresh()
            return script
        except Exception as e:
            print(f"Error setting script info: {e}")
            return None

    def get_associated_runs(self):
        try:
            from gemini.api.script_run import ScriptRun
            current_id = self.id
            script_runs = ScriptRunsViewModel.search(script_id=current_id)
            if not script_runs or len(script_runs) == 0:
                print("No associated runs found.")
                return None
            runs = [ScriptRun.model_validate(script_run) for script_run in script_runs]
            return runs
        except Exception as e:
            print(f"Error getting associated runs: {e}")
            return None

    def create_new_run(self, script_run_info: dict):
        try:
            from gemini.api.script_run import ScriptRun
            new_script_run = ScriptRun.create(
                script_run_info=script_run_info,
                script_name=self.script_name
            )
            if not new_script_run:
                print("Failed to create new script run.")
                return None
            return new_script_run
        except Exception as e:
            print(f"Error creating script run: {e}")
            return None

    def get_associated_experiments(self):
        try:
            from gemini.api.experiment import Experiment
            current_id = self.id
            experiment_scripts = ExperimentScriptsViewModel.search(script_id=current_id)
            if not experiment_scripts or len(experiment_scripts) == 0:
                print("No associated experiments found.")
                return None
            experiments = [Experiment.model_validate(experiment) for experiment in experiment_scripts]
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
            existing_association = ExperimentScriptModel.get_by_parameters(
                experiment_id=experiment.id,
                script_id=self.id
            )
            if existing_association:
                print(f"Script {self.script_name} is already associated with experiment {experiment_name}.")
                return self
            new_association = ExperimentScriptModel.get_or_create(
                experiment_id=experiment.id,
                script_id=self.id
            )
            if not new_association:
                print(f"Failed to associate script {self.script_name} with experiment {experiment_name}.")
                return None
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error associating script with experiment: {e}")
            return None


    def unassociate_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return None
            existing_association = ExperimentScriptModel.get_by_parameters(
                experiment_id=experiment.id,
                script_id=self.id
            )
            if not existing_association:
                print(f"Script {self.script_name} is not associated with experiment {experiment_name}.")
                return self
            is_deleted = ExperimentScriptModel.delete(existing_association)
            if not is_deleted:
                print(f"Failed to unassociate script {self.script_name} from experiment {experiment_name}.")
                return None
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error unassociating script from experiment: {e}")
            return None

    def belongs_to_experiment(self, experiment_name: str) -> bool:
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return False
            association_exists = ExperimentScriptModel.exists(
                experiment_id=experiment.id,
                script_id=self.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking if script belongs to experiment: {e}")
            return
        
    def get_associated_datasets(self):
        try:
            from gemini.api.dataset import Dataset
            current_id = self.id
            script_datasets = ScriptDatasetsViewModel.search(script_id=current_id)
            if not script_datasets or len(script_datasets) == 0:
                print("No associated datasets found.")
                return None
            datasets = [Dataset.model_validate(script_dataset) for script_dataset in script_datasets]
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
    ) -> Optional[Dataset]:
        try:
            from gemini.api.dataset import Dataset
            dataset = Dataset.create(
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                collection_date=collection_date,
                experiment_name=experiment_name,
                dataset_type=GEMINIDatasetType.Script
            )
            if not dataset:
                print("Failed to create new dataset.")
                return None
            dataset = self.associate_dataset(dataset_name=dataset_name)
            return dataset
        except Exception as e:
            print(f"Error creating new dataset: {e}")
            return None
        
    def associate_dataset(self, dataset_name: str):
        try:
            from gemini.api.dataset import Dataset
            dataset = Dataset.get(dataset_name=dataset_name)
            if not dataset:
                print(f"Dataset {dataset_name} does not exist.")
                return None
            existing_association = ScriptDatasetModel.get_by_parameters(
                script_id=self.id,
                dataset_id=dataset.id
            )
            if existing_association:
                print(f"Script {self.script_name} is already associated with dataset {dataset_name}.")
                return self
            new_association = ScriptDatasetModel.get_or_create(
                script_id=self.id,
                dataset_id=dataset.id
            )
            if not new_association:
                print(f"Failed to associate script {self.script_name} with dataset {dataset_name}.")
                return None
            self.refresh()
            return dataset
        except Exception as e:
            print(f"Error associating script with dataset: {e}")
            return None

    def insert_record(
        self,
        timestamp: datetime = None,
        collection_date: date = None,
        script_data: dict = {},
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
            
            if not script_data and not record_file:
                raise ValueError("Either script_data or record_file must be provided.")
            
            timestamp = timestamp if timestamp else datetime.now()
            collection_date = collection_date if collection_date else timestamp.date()
            if not dataset_name:
                dataset_name = f"{self.script_name} Dataset {collection_date}"
            script_name = self.script_name
            script_record = ScriptRecord.create(
                timestamp=timestamp,
                collection_date=collection_date,
                script_name=script_name,
                script_data=script_data,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                record_file=record_file,
                record_info=record_info,
                insert_on_create=False
            )
            success, inserted_record_ids = ScriptRecord.insert([script_record])
            if not success:
                raise Exception("Failed to insert script record.")
            return success, inserted_record_ids
        except Exception as e:
            print(f"Error inserting script record: {e}")
            return False, []
        
    def insert_records(
        self,
        timestamps: List[datetime] = None,
        collection_date: date = None,
        script_data: List[dict] = [],
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
            
            if len(script_data) != len(timestamps):
                raise ValueError("script_data must have the same length as timestamps.")
            
            if record_files and len(record_files) != len(timestamps):
                raise ValueError("record_files must have the same length as timestamps.")
            
            collection_date = collection_date if collection_date else timestamps[0].date()
            
            if not dataset_name:
                dataset_name = f"{self.script_name} Dataset {collection_date}"
            
            script_records = []
            timestamps_length = len(timestamps)

            for i in tqdm(range(timestamps_length), desc="Arranging Records for Script " + self.script_name):
                script_record = ScriptRecord.create(
                    timestamp = timestamps[i],
                    collection_date = collection_date,
                    script_name= self.script_name,
                    script_data = script_data[i]  if script_data else {},
                    dataset_name = dataset_name,
                    experiment_name = experiment_name,
                    season_name = season_name,
                    site_name = site_name,
                    record_file= record_files[i] if record_files else None,
                    record_info = record_info[i] if record_info else {},
                    insert_on_create=False
                )
                script_records.append(script_record)

            success, inserted_record_ids = ScriptRecord.insert(script_records)
            if not success:
                print("Failed to insert script records.")
                return False, []
            return success, inserted_record_ids
        except Exception as e:
            print(f"Error inserting script records: {e}")
            return False, []
        
    def search_records(
        self,
        collection_date: date = None,
        dataset_name: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        record_info: dict = None
    ) -> List[ScriptRecord]:
        try:
            record_info = record_info if record_info else {}
            record_info = {k: v for k, v in record_info.items() if v is not None}

            records = ScriptRecord.search(
                collection_date=collection_date,
                dataset_name=dataset_name,
                script_name=self.script_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                record_info=record_info
            )
            return records
        except Exception as e:
            print(f"Error searching script records: {e}")
            return []
        
    def filter_records(
        self,
        start_timestamp: Optional[datetime] = None,
        end_timestamp: Optional[datetime] = None,
        dataset_names: Optional[List[str]] = None,
        experiment_names: Optional[List[str]] = None,
        season_names: Optional[List[str]] = None,
        site_names: Optional[List[str]] = None
    ) -> List[ScriptRecord]:
        try:
            records = ScriptRecord.filter(
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
                script_names=[self.script_name],
                dataset_names=dataset_names,
                experiment_names=experiment_names,
                season_names=season_names,
                site_names=site_names
            )
            return records
        except Exception as e:
            print(f"Error filtering script records: {e}")
            return []
            

