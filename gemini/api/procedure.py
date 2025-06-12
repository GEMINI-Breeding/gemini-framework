from typing import Optional, List
from uuid import UUID
from tqdm import tqdm

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.dataset import Dataset, GEMINIDatasetType
from gemini.api.procedure_run import ProcedureRun
from gemini.api.procedure_record import ProcedureRecord
from gemini.db.models.procedures import ProcedureModel
from gemini.db.models.procedure_runs import ProcedureRunModel
from gemini.db.models.associations import ExperimentProcedureModel, ProcedureDatasetModel
from gemini.db.models.views.experiment_views import ExperimentProceduresViewModel
from gemini.db.models.views.dataset_views import ProcedureDatasetsViewModel
from gemini.db.models.views.run_views import ProcedureRunsViewModel

from datetime import date, datetime

class Procedure(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "procedure_id"))

    procedure_name: str
    procedure_info: Optional[dict] = None

    def __str__(self):
        return f"Procedure(name={self.procedure_name}, id={self.id})"
    
    def __repr__(self):
        return f"Procedure(procedure_name={self.procedure_name}, id={self.id})"
    
    @classmethod
    def exists(
        cls,
        procedure_name: str
    ) -> bool:
        try:
            exists = ProcedureModel.exists(procedure_name=procedure_name)
            return exists
        except Exception as e:
            print(f"Error checking existence of procedure: {e}")
            return False
        
    @classmethod
    def create(
        cls,
        procedure_name: str,
        procedure_info: dict = {},
        experiment_name: str = None
    ) -> Optional["Procedure"]:
        try:
            db_instance = ProcedureModel.get_or_create(
                procedure_name=procedure_name,
                procedure_info=procedure_info,
            )
            procedure = cls.model_validate(db_instance)
            if experiment_name:
                procedure.associate_experiment(experiment_name)
            return procedure
        except Exception as e:
            print(f"Error creating procedure: {e}")
            return None
        
    @classmethod
    def get(
        cls,
        procedure_name: str,
        experiment_name: str = None
    ) -> Optional["Procedure"]:
        try:
            db_instance = ExperimentProceduresViewModel.get_by_parameters(
                procedure_name=procedure_name,
                experiment_name=experiment_name
            )
            if not db_instance:
                print(f"Procedure with name {procedure_name} not found.")
                return None
            procedure = cls.model_validate(db_instance)
            return procedure
        except Exception as e:
            print(f"Error getting procedure: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["Procedure"]:
        try:
            db_instance = ProcedureModel.get(id)
            if not db_instance:
                print(f"Procedure with ID {id} does not exist.")
                return None
            procedure = cls.model_validate(db_instance)
            return procedure
        except Exception as e:
            print(f"Error getting procedure by ID: {e}")
            return None
        
    @classmethod
    def get_all(cls) -> Optional[List["Procedure"]]:
        try:
            procedures = ProcedureModel.all()
            if not procedures or len(procedures) == 0:
                print("No procedures found.")
                return None
            procedures = [cls.model_validate(procedure) for procedure in procedures]
            return procedures
        except Exception as e:
            print(f"Error getting all procedures: {e}")
            return None
        
    @classmethod
    def search(
        cls,
        procedure_name: str = None,
        procedure_info: dict = None,
        experiment_name: str = None
    ) -> Optional[List["Procedure"]]:
        try:
            if not any([procedure_name, procedure_info, experiment_name]):
                print("At least one search parameter must be provided.")
                return None
            procedures = ExperimentProceduresViewModel.search(
                procedure_name=procedure_name,
                procedure_info=procedure_info,
                experiment_name=experiment_name
            )
            if not procedures or len(procedures) == 0:
                print("No procedures found with the provided search parameters.")
                return None
            procedures = [cls.model_validate(procedure) for procedure in procedures]
            return procedures
        except Exception as e:
            print(f"Error searching procedures: {e}")
            return None
        
    def update(
        self,
        procedure_name: str = None,
        procedure_info: dict = None
    ) -> Optional["Procedure"]:
        try:
            if not any([procedure_name, procedure_info]):
                print("At least one parameter must be provided.")
                return None
            current_id = self.id
            procedure = ProcedureModel.get(current_id)
            if not procedure:
                print(f"Procedure with ID {current_id} does not exist.")
                return None
            procedure = ProcedureModel.update(
                procedure,
                procedure_name=procedure_name,
                procedure_info=procedure_info
            )
            procedure = self.model_validate(procedure)
            self.refresh()
            return procedure
        except Exception as e:
            print(f"Error updating procedure: {e}")
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            procedure = ProcedureModel.get(current_id)
            if not procedure:
                print(f"Procedure with ID {current_id} does not exist.")
                return False
            ProcedureModel.delete(procedure)
            return True
        except Exception as e:
            print(f"Error deleting procedure: {e}")
            return False
        
    def refresh(self) -> Optional["Procedure"]:
        try:
            db_instance = ProcedureModel.get(self.id)
            if not db_instance:
                print(f"Procedure with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing procedure: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            procedure = ProcedureModel.get(current_id)
            if not procedure:
                print(f"Procedure with ID {current_id} does not exist.")
                return None
            procedure_info = procedure.procedure_info
            if not procedure_info:
                print("Procedure info is empty.")
                return None
            return procedure_info
        except Exception as e:
            print(f"Error getting procedure info: {e}")
            return None

    def set_info(self, procedure_info: dict) -> Optional["Procedure"]:
        try:
            current_id = self.id
            procedure = ProcedureModel.get(current_id)
            if not procedure:
                print(f"Procedure with ID {current_id} does not exist.")
                return None
            procedure = ProcedureModel.update(
                procedure,
                procedure_info=procedure_info
            )
            procedure = self.model_validate(procedure)
            self.refresh()
            return procedure
        except Exception as e:
            print(f"Error setting procedure info: {e}")
            return None        
    
    def get_associated_runs(self):
        try:
            from gemini.api.procedure_run import ProcedureRun
            current_id = self.id
            procedure_runs = ProcedureRunsViewModel.search(procedure_id=current_id)
            if not procedure_runs or len(procedure_runs) == 0:
                print("No associated runs found.")
                return None
            procedure_runs = [ProcedureRun.model_validate(run) for run in procedure_runs]
            return procedure_runs
        except Exception as e:
            print(f"Error getting associated runs: {e}")
            return None
        
    def create_new_run(self, procedure_run_info: dict = None):
        try:
            from gemini.api.procedure_run import ProcedureRun
            new_procedure_run = ProcedureRun.create(
                procedure_run_info=procedure_run_info,
                procedure_name=self.procedure_name
            )
            if not new_procedure_run:
                print("Failed to create new procedure run.")
                return None
            return new_procedure_run
        except Exception as e:
            print(f"Error creating procedure run: {e}")
            return None

    def get_associated_experiments(self):
        try:
            from gemini.api.experiment import Experiment
            experiment_procedures = ExperimentProceduresViewModel.search(procedure_id=self.id)
            if not experiment_procedures or len(experiment_procedures) == 0:
                print("No associated experiments found.")
                return None
            experiments = [Experiment.model_validate(exp) for exp in experiment_procedures]
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
            existing_association = ExperimentProcedureModel.get_by_parameters(
                experiment_id=experiment.id,
                procedure_id=self.id
            )
            if existing_association:
                print(f"Procedure {self.procedure_name} is already associated with experiment {experiment_name}.")
                return self
            new_association = ExperimentProcedureModel.get_or_create(
                experiment_id=experiment.id,
                procedure_id=self.id
            )
            if not new_association:
                print(f"Failed to associate procedure {self.procedure_name} with experiment {experiment_name}.")
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
            existing_association = ExperimentProcedureModel.get_by_parameters(
                experiment_id=experiment.id,
                procedure_id=self.id
            )
            if not existing_association:
                print(f"Procedure {self.procedure_name} is not associated with experiment {experiment_name}.")
                return None
            is_deleted = ExperimentProcedureModel.delete(existing_association)
            if not is_deleted:
                print(f"Failed to disassociate procedure {self.procedure_name} from experiment {experiment_name}.")
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
            association_exists = ExperimentProcedureModel.exists(
                experiment_id=experiment.id,
                procedure_id=self.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking experiment membership: {e}")
            return False
        
    def get_associated_datasets(self) -> List["Dataset"]:
        try:
            from gemini.api.dataset import Dataset
            datasets = ProcedureDatasetsViewModel.search(procedure_id=self.id)
            if not datasets or len(datasets) == 0:
                print("No associated datasets found.")
                return None
            datasets = [Dataset.model_validate(dataset) for dataset in datasets]
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
    ) -> Optional["Dataset"]:
        try:
            from gemini.api.dataset import Dataset
            dataset = Dataset.create(
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                collection_date=collection_date,
                experiment_name=experiment_name,
                dataset_type=GEMINIDatasetType.Procedure
            )
            if not dataset:
                print("Failed to create new dataset.")
                return None
            dataset = self.associate_dataset(dataset_name)
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
            existing_association = ProcedureDatasetModel.get_by_parameters(
                procedure_id=self.id,
                dataset_id=dataset.id
            )
            if existing_association:
                print(f"Dataset {dataset_name} is already associated with procedure {self.procedure_name}.")
                return self
            new_association = ProcedureDatasetModel.get_or_create(
                procedure_id=self.id,
                dataset_id=dataset.id
            )
            if not new_association:
                print(f"Failed to associate dataset {dataset_name} with procedure {self.procedure_name}.")
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
        procedure_data: dict = {},
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
            
            if not procedure_data and not record_file:
                raise ValueError("Either procedure_data or record_file must be provided.")
            
            timestamp = timestamp if timestamp else datetime.now()
            collection_date = collection_date if collection_date else timestamp.date()
            if not dataset_name:
                dataset_name = f"{self.procedure_name} Dataset {collection_date}"
            procedure_name = self.procedure_name
            procedure_record = ProcedureRecord.create(
                timestamp=timestamp,
                collection_date=collection_date,
                procedure_name=procedure_name,
                procedure_data=procedure_data,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                record_file=record_file,
                record_info=record_info,
                insert_on_create=False
            )
            success, inserted_record_ids = ProcedureRecord.insert([procedure_record])
            if not success:
                raise Exception("Failed to insert procedure record.")
            return success, inserted_record_ids
        except Exception as e:
            print(f"Error inserting procedure record: {e}")
            return False, []
        
    def insert_records(
        self,
        timestamps: List[datetime] = None,
        collection_date: date = None,
        procedure_data: List[dict] = [],
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
            
            if procedure_data and len(procedure_data) != len(timestamps):
                raise ValueError("procedure_data must have the same length as timestamps.")
            
            if record_files and len(record_files) != len(timestamps):
                raise ValueError("record_files must have the same length as timestamps.")
            
            collection_date = collection_date if collection_date else timestamps[0].date()
            
            if not dataset_name:
                dataset_name = f"{self.procedure_name} Dataset {collection_date}"
            
            procedure_records = []
            timestamps_length = len(timestamps)

            for i in tqdm(range(timestamps_length), desc="Arranging Records for Procedure " + self.procedure_name):
                procedure_record = ProcedureRecord.create(
                    timestamp = timestamps[i],
                    collection_date = collection_date,
                    procedure_name= self.procedure_name,
                    procedure_data = procedure_data[i]  if procedure_data else {},
                    dataset_name = dataset_name,
                    experiment_name = experiment_name,
                    season_name = season_name,
                    site_name = site_name,
                    record_file= record_files[i] if record_files else None,
                    record_info = record_info[i] if record_info else {},
                    insert_on_create=False
                )
                procedure_records.append(procedure_record)

            success, inserted_record_ids = ProcedureRecord.insert(procedure_records)
            if not success:
                print("Failed to insert procedure records.")
                return False, []
            return success, inserted_record_ids
        except Exception as e:
            print(f"Error inserting procedure records: {e}")
            return False, []
        
    def search_records(
        self,
        collection_date: date = None,
        dataset_name: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        record_info: dict = None
    ) -> List[ProcedureRecord]:
        try:
            record_info = record_info if record_info else {}
            record_info = {k: v for k, v in record_info.items() if v is not None}

            records = ProcedureRecord.search(
                collection_date=collection_date,
                dataset_name=dataset_name,
                procedure_name=self.procedure_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                record_info=record_info
            )
            return records
        except Exception as e:
            print(f"Error searching procedure records: {e}")
            return []