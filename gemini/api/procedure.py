from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.procedure_record import ProcedureRecord
from gemini.db.models.procedures import ProcedureModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.views.experiment_views import ExperimentProceduresViewModel

from datetime import date, datetime

class Procedure(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "procedure_id"))

    procedure_name: str
    procedure_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        procedure_name: str,
        procedure_info: dict = {},
        experiment_name: str = "Default",
    ) -> "Procedure":
        try:
            db_instance = ProcedureModel.get_or_create(
                procedure_name=procedure_name,
                procedure_info=procedure_info,
            )
            procedure = cls.model_validate(db_instance)
            experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
            if experiment:
                experiment.procedures.append(procedure)
            return procedure
        except Exception as e:
            raise e
    
    @classmethod
    def get(cls, procedure_name: str) -> "Procedure":
        try:
            db_instance = ProcedureModel.get_by_parameters(
                procedure_name=procedure_name,
            )
            procedure = cls.model_validate(db_instance)
            return procedure
        except Exception as e:
            raise e
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Procedure":
        try:
            db_instance = ProcedureModel.get(id)
            procedure = cls.model_validate(db_instance)
            return procedure
        except Exception as e:
            raise e
        
    @classmethod
    def get_all(cls) -> List["Procedure"]:
        try:
            procedures = ProcedureModel.all()
            procedures = [cls.model_validate(procedure) for procedure in procedures]
            return procedures
        except Exception as e:
            raise e
        

    @classmethod
    def search(cls, **search_parameters) -> List["Procedure"]:
        try:
            procedures = ExperimentProceduresViewModel.search(**search_parameters)
            procedures = [cls.model_validate(procedure) for procedure in procedures]
            return procedures if procedures else None
        except Exception as e:
            raise e
        

    def update(self, **update_parameters) -> "Procedure":
        try:
            current_id = self.id
            procedure = ProcedureModel.get(current_id)
            procedure = ProcedureModel.update(current_id, **update_parameters)
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
                    actual_value = getattr(instance, key)
                    setattr(self, key, actual_value)
            return self
        except Exception as e:
            raise e 
        

    def add_record(
        self,
        record: ProcedureRecord
    ) -> bool:
        try:
            if record.timestamp is None:
                record.timestamp = datetime.now()
            if record.collection_date is None:
                record.collection_date = record.timestamp.date()
            if record.dataset_name is None:
                record.dataset_name = f"{self.procedure_name} Dataset"
            if record.procedure_name is None:
                record.procedure_name = self.procedure_name
            if record.record_info is None:
                record.record_info = {}

            record.procedure_id = self.id

            success = ProcedureRecord.add([record])
            return success
        except Exception as e:
            return False
        

    def add_records(
        self,
        records: List[ProcedureRecord]
    ) -> bool:
        try:
            for record in records:
                if record.timestamp is None:
                    record.timestamp = datetime.now()
                if record.collection_date is None:
                    record.collection_date = record.timestamp.date()
                if record.dataset_name is None:
                    record.dataset_name = f"{self.procedure_name} Dataset"
                if record.procedure_name is None:
                    record.procedure_name = self.procedure_name
                if record.record_info is None:
                    record.record_info = {}

                record.procedure_id = self.id
            success = ProcedureRecord.add(records)
            return success
        except Exception as e:
            return False
        
    def get_records(
            self,
            collection_date: date = None,
            experiment_name: str = None,
            season_name: str = None,
            site_name: str = None,
            plot_number: int = None,
            plot_row_number: int = None,
            plot_column_number: int = None,
            record_info: dict = None
    ) -> List[ProcedureRecord]:
        try:
            record_info = record_info if record_info else {}
            record_info = {k: v for k, v in record_info.items() if v is not None}

            records = ProcedureRecord.search(
                procedure_id=self.id,
                collection_date=collection_date,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                record_info=record_info
            )
            return records
        except Exception as e:
            raise e