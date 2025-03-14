from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.db.models.procedure_runs import ProcedureRunModel
from gemini.db.models.procedures import ProcedureModel



class ProcedureRun(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "procedure_run_id"))

    procedure_id : UUID
    procedure_run_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        procedure_run_info: dict = {},
        procedure_name: str = None,
    ) -> "ProcedureRun":
        try:
            db_procedure = ProcedureModel.get_by_parameters(procedure_name=procedure_name)
            if not db_procedure:
                raise Exception(f"Procedure with name {procedure_name} does not exist.")
            db_instance = ProcedureRunModel.get_or_create(
                procedure_run_info=procedure_run_info,
                procedure_id=db_procedure.id
            )
            procedure_run = cls.model_validate(db_instance)
            return procedure_run
        except Exception as e:
            raise e
        
    @classmethod
    def get(cls, procedure_run_info: dict, procedure_name: str = None) -> "ProcedureRun":
        try:
            db_procedure = ProcedureModel.get_by_parameters(procedure_name=procedure_name)
            if not db_procedure:
                raise Exception(f"Procedure with name {procedure_name} does not exist.")
            db_instance = ProcedureRunModel.get_by_parameters(
                procedure_run_info=procedure_run_info,
                procedure_id=db_procedure.id
            )
            procedure_run = cls.model_validate(db_instance) if db_instance else None
            return procedure_run
        except Exception as e:
            raise e
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "ProcedureRun":
        try:
            db_instance = ProcedureRunModel.get(id)
            procedure_run = cls.model_validate(db_instance) if db_instance else None
            return procedure_run
        except Exception as e:
            raise e
        
    @classmethod
    def get_all(cls) -> List["ProcedureRun"]:
        try:
            db_instances = ProcedureRunModel.all()
            procedure_runs = [cls.model_validate(db_instance) for db_instance in db_instances]
            return procedure_runs if procedure_runs else None
        except Exception as e:
            raise e
        
    @classmethod
    def search(
        cls,
        procedure_run_info: dict = None,
        procedure_name: str = None
    ) -> List["ProcedureRun"]:
        try:
            if not procedure_name and not procedure_run_info:
                raise Exception("Either procedure_name or procedure_run_info must be provided.")
            
            db_model = ProcedureModel.get_by_parameters(procedure_name=procedure_name)
            if not db_model:
                raise Exception(f"Procedure with name {procedure_name} does not exist.")
            
            procedure_runs = ProcedureRunModel.search(
                procedure_run_info=procedure_run_info,
                procedure_id=db_model.id
            )
            procedure_runs = [cls.model_validate(procedure_run) for procedure_run in procedure_runs]
            return procedure_runs if procedure_runs else None
        except Exception as e:
            raise e
        
    def update(
        self,
        procedure_run_info: dict = None
    ) -> "ProcedureRun":
        try:
            if not procedure_run_info:
                raise Exception("procedure_run_info must be provided.")
            current_id = self.id
            procedure_run = ProcedureRunModel.get(id=current_id)
            procedure_run = ProcedureRunModel.update(
                procedure_run,
                procedure_run_info=procedure_run_info
            )
            procedure_run = self.model_validate(procedure_run)
            self.refresh()
            return procedure_run 
        except Exception as e:
            raise e
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            procedure_run = ProcedureRunModel.get(current_id)
            ProcedureRunModel.delete(procedure_run)
            return True
        except Exception as e:
            raise e
        
    def refresh(self) -> "ProcedureRun":
        try:
            db_instance = ProcedureRunModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e