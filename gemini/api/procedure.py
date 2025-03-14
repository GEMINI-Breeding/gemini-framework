from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.dataset import Dataset, GEMINIDatasetType
from gemini.api.procedure_run import ProcedureRun
from gemini.api.procedure_record import ProcedureRecord
from gemini.db.models.procedures import ProcedureModel
from gemini.db.models.procedure_runs import ProcedureRunModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.associations import ExperimentProcedureModel, ProcedureDatasetModel
from gemini.db.models.views.experiment_views import ExperimentProceduresViewModel
from gemini.db.models.views.dataset_views import ProcedureDatasetsViewModel

from datetime import date

class Procedure(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "procedure_id"))

    procedure_name: str
    procedure_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        procedure_name: str,
        procedure_info: dict = {},
        experiment_name: str = None,
    ) -> "Procedure":
        try:
            db_instance = ProcedureModel.get_or_create(
                procedure_name=procedure_name,
                procedure_info=procedure_info,
            )

            if experiment_name:
                db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
                if db_experiment:
                    ExperimentProcedureModel.get_or_create(experiment_id=db_experiment.id, procedure_id=db_instance.id)

            procedure = cls.model_validate(db_instance)
            return procedure

        except Exception as e:
            raise e
    
    @classmethod
    def get(cls, procedure_name: str, experiment_name: str = None) -> "Procedure":
        try:
            db_instance = ExperimentProceduresViewModel.get_by_parameters(
                procedure_name=procedure_name,
                experiment_name=experiment_name
            )
            procedure = cls.model_validate(db_instance) if db_instance else None
            return procedure
        except Exception as e:
            raise e
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Procedure":
        try:
            db_instance = ProcedureModel.get(id)
            procedure = cls.model_validate(db_instance) if db_instance else None
            return procedure
        except Exception as e:
            raise e
        
    @classmethod
    def get_all(cls) -> List["Procedure"]:
        try:
            procedures = ProcedureModel.all()
            procedures = [cls.model_validate(procedure) for procedure in procedures]
            return procedures if procedures else None
        except Exception as e:
            raise e
        

    @classmethod
    def search(
        cls, 
        experiment_name: str = None,
        procedure_name: str = None,
        procedure_info: dict = None
    ) -> List["Procedure"]:
        try:
            if not procedure_info and not procedure_name and not experiment_name:
                raise Exception("At least one search parameter must be provided.")

            procedures = ExperimentProceduresViewModel.search(
                experiment_name=experiment_name,
                procedure_name=procedure_name,
                procedure_info=procedure_info
            )
            procedures = [cls.model_validate(procedure) for procedure in procedures]
            return procedures if procedures else None
        except Exception as e:
            raise e
        
    def update(
        self,
        procedure_name: str = None,
        procedure_info: dict = None
    ) -> "Procedure":
        try:
            if  not procedure_info and not procedure_name:
                raise Exception("At least one parameter must be provided.")
            
            current_id = self.id
            procedure = ProcedureModel.get(current_id)
            procedure = ProcedureModel.update(
                procedure,
                procedure_name=procedure_name,
                procedure_info=procedure_info
            )
            procedure = self.model_validate(procedure)
            self.refresh()
            return procedure
        except Exception as e:
            raise e
        
    
    def delete(self) -> bool:
        try:
            current_id = self.id
            procedure = ProcedureModel.get(current_id)
            ProcedureModel.delete(procedure)
            return True
        except Exception as e:
            return False
        

    def refresh(self) -> "Procedure":
        try:
            db_instance = ProcedureModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e 
        
    def get_datasets(self) -> List["Dataset"]:
        try:
            procedure = ProcedureModel.get(self.id)
            datasets = ProcedureDatasetsViewModel.search(procedure_id=procedure.id)
            datasets = [Dataset.model_validate(dataset) for dataset in datasets]
            return datasets if datasets else None
        except Exception as e:
            raise e

    def create_dataset(
        self,
        dataset_name: str,
        dataset_info: dict = {},
        collection_date: date = None,
        experiment_name: str = None
    ) -> Dataset:
        try:
            dataset = Dataset.create(
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                collection_date=collection_date,
                experiment_name=experiment_name,
                dataset_type=GEMINIDatasetType.Procedure
            )
            ProcedureDatasetModel.get_or_create(procedure_id=self.id, dataset_id=dataset.id)
            return dataset
        except Exception as e:
            raise e


    def get_runs(self) -> List[ProcedureRun]:
        try:
            procedure = ProcedureModel.get(self.id)
            runs = ProcedureRunModel.search(procedure_id=procedure.id)
            runs = [ProcedureRun.model_validate(run) for run in runs]
            return runs if runs else None
        except Exception as e:
            raise e

    def create_run(
        self,
        procedure_run_info: dict = None,
    ) -> ProcedureRun:
        try:
            run = ProcedureRun.create(
                procedure_run_info=procedure_run_info,
                procedure_name=self.procedure_name
            )
            return run
        except Exception as e:
            raise e
        
    
    def add_record(
        self,
        record: ProcedureRecord
    ) -> bool:
        try:
            record.procedure_id = self.id
            record.procedure_name = self.procedure_name
            record.dataset_name = f"{self.procedure_name} Dataset"
            record.timestamp = record.timestamp if record.timestamp else date.today()

            success = ProcedureRecord.add([record])
            return success
        except Exception as e:
            raise e
        
    def add_records(
        self,
        records: List[ProcedureRecord]
    ) -> bool:
        try:
            for record in records:
                record.procedure_id = self.id
                record.procedure_name = self.procedure_name
                record.dataset_name = f"{self.procedure_name} Dataset"
                record.timestamp = record.timestamp if record.timestamp else date.today()

            success = ProcedureRecord.add(records)
            return success
        except Exception as e:
            raise e
        
    def get_records(
        self,
        collection_date: date = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        record_info: dict = None
    ) -> List[ProcedureRecord]:
        try:
            record_info = record_info if record_info else {}
            record_info = {k: v for k, v in record_info.items() if v is not None}

            records = ProcedureRecord.search(
                procedure_name=self.procedure_name,
                collection_date=collection_date,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                record_info=record_info
            )
            return records
        except Exception as e:
            raise e

      