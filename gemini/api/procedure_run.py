from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.db.models.procedure_runs import ProcedureRunModel
from gemini.db.models.procedures import ProcedureModel
from gemini.db.models.views.run_views import ProcedureRunsViewModel


class ProcedureRun(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "procedure_run_id"))

    procedure_id : Optional[ID]
    procedure_run_info: Optional[dict] = None

    def __str__(self) -> str:
        return f"ProcedureRun(id={self.id}, procedure_id={self.procedure_id}, procedure_run_info={self.procedure_run_info})"
    
    def __repr__(self) -> str:
        return f"ProcedureRun(id={self.id}, procedure_id={self.procedure_id}, procedure_run_info={self.procedure_run_info})"
    
    @classmethod
    def exists(
        cls,
        procedure_run_info: dict,
        procedure_name: str = None
    ) -> bool:
        try:
            exists = ProcedureRunsViewModel.exists(
                procedure_run_info=procedure_run_info,
                procedure_name=procedure_name
            )
            return exists
        except Exception as e:
            print(f"Error checking existence of ProcedureRun: {e}")
            return False
        
    @classmethod
    def create(
        cls,
        procedure_run_info: dict = {},
        procedure_name: str = None,
    ) -> Optional["ProcedureRun"]:
        try:
            db_instance = ProcedureRunModel.get_or_create(
                procedure_run_info=procedure_run_info,
            )
            procedure_run = cls.model_validate(db_instance)
            if procedure_name:
                procedure_run.associate_procedure(procedure_name)
            return procedure_run
        except Exception as e:
            print(f"Error creating ProcedureRun: {e}")
            return None
        
    @classmethod
    def get(cls, procedure_run_info: dict, procedure_name: str = None) -> Optional["ProcedureRun"]:
        try:
            db_instance = ProcedureRunModel.get_by_parameters(
                procedure_run_info=procedure_run_info,
                procedure_name=procedure_name
            )
            if not db_instance:
                print(f"ProcedureRun with info {procedure_run_info} and name {procedure_name} not found.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting ProcedureRun: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["ProcedureRun"]:
        try:
            db_instance = ProcedureRunModel.get(id)
            if not db_instance:
                print(f"ProcedureRun with ID {id} does not exist.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting ProcedureRun by ID: {e}")
            return None
        
    @classmethod
    def get_all(cls) -> Optional[List["ProcedureRun"]]:
        try:
            procedure_runs = ProcedureRunModel.all()
            if not procedure_runs or len(procedure_runs) == 0:
                print("No ProcedureRuns found.")
                return None
            procedure_runs = [cls.model_validate(procedure_run) for procedure_run in procedure_runs]
            return procedure_runs
        except Exception as e:
            print(f"Error getting all ProcedureRuns: {e}")
            return None
        
    @classmethod
    def search(
        cls,
        procedure_run_info: dict = None,
        procedure_name: str = None
    ) -> Optional[List["ProcedureRun"]]:
        try:
            if not any([procedure_name, procedure_run_info]):
                print("Either procedure_name or procedure_run_info must be provided.")
                return None
            procedure_runs = ProcedureRunsViewModel.search(
                procedure_run_info=procedure_run_info,
                procedure_name=procedure_name
            )
            if not procedure_runs or len(procedure_runs) == 0:
                print("No ProcedureRuns found with the provided search parameters.")
                return None
            procedure_runs = [cls.model_validate(procedure_run) for procedure_run in procedure_runs]
            return procedure_runs
        except Exception as e:
            print(f"Error searching ProcedureRuns: {e}")
            return None
        
    def update(self, procedure_run_info: dict = None) -> Optional["ProcedureRun"]:
        try:
            if not procedure_run_info:
                print("procedure_run_info must be provided.")
                return None
            current_id = self.id
            procedure_run = ProcedureRunModel.get(id=current_id)
            if not procedure_run:
                print(f"ProcedureRun with ID {current_id} does not exist.")
                return None
            procedure_run = ProcedureRunModel.update(
                procedure_run,
                procedure_run_info=procedure_run_info
            )
            instance = self.model_validate(procedure_run)
            self.refresh()
            return instance 
        except Exception as e:
            print(f"Error updating ProcedureRun: {e}")
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            procedure_run = ProcedureRunModel.get(current_id)
            if not procedure_run:
                print(f"ProcedureRun with ID {current_id} does not exist.")
                return False
            ProcedureRunModel.delete(procedure_run)
            return True
        except Exception as e:
            print(f"Error deleting ProcedureRun: {e}")
            return False
        
    def refresh(self) -> Optional["ProcedureRun"]:
        try:
            db_instance = ProcedureRunModel.get(self.id)
            if not db_instance:
                print(f"ProcedureRun with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing ProcedureRun: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            procedure_run = ProcedureRunModel.get(current_id)
            if not procedure_run:
                print(f"ProcedureRun with ID {current_id} does not exist.")
                return None
            procedure_run_info = procedure_run.procedure_run_info
            if not procedure_run_info:
                print("ProcedureRun info is empty.")
                return None  # Return None if info is empty/None
            return procedure_run_info
        except Exception as e:
            print(f"Error getting ProcedureRun info: {e}")
            return None
        
    def set_info(self, procedure_run_info: dict) -> Optional["ProcedureRun"]:
        try:
            current_id = self.id
            procedure_run = ProcedureRunModel.get(current_id)
            if not procedure_run:
                print(f"ProcedureRun with ID {current_id} does not exist.")
                return None
            procedure_run = ProcedureRunModel.update(
                procedure_run,
                procedure_run_info=procedure_run_info,
            )
            instance = self.model_validate(procedure_run)
            self.refresh()
            return instance
        except Exception as e:
            print(f"Error setting ProcedureRun info: {e}")
            return None
        
    def get_associated_procedure(self):
        try:
            from gemini.api.procedure import Procedure
            if not self.procedure_id:
                print("Procedure ID is not set.")
                return None
            procedure = Procedure.get_by_id(self.procedure_id)
            if not procedure:
                print(f"Procedure with ID {self.procedure_id} does not exist.")
                return None
            return procedure
        except Exception as e:
            print(f"Error getting associated Procedure: {e}")
            return None

    def associate_procedure(self, procedure_name: str):
        try:
            from gemini.api.procedure import Procedure
            procedure = Procedure.get(procedure_name=procedure_name)
            if not procedure:
                print(f"Procedure with name {procedure_name} does not exist.")
                return None
            existing_association = ProcedureRunModel.get_by_parameters(
                procedure_id=procedure.id,
                id=self.id
            )
            if existing_association:
                print(f"ProcedureRun with ID {self.id} is already associated with Procedure {procedure_name}.")
                return self
            db_procedure_run = ProcedureRunModel.get(self.id)
            db_procedure_run = ProcedureRunModel.update_parameter(
                db_procedure_run,
                "procedure_id",
                procedure.id
            )
            self.refresh()
            return procedure
        except Exception as e:
            print(f"Error associating Procedure with ProcedureRun: {e}")
            return None
    
    def belongs_to_procedure(self, procedure_name: str) -> bool:
        try:
            from gemini.api.procedure import Procedure
            procedure = Procedure.get(procedure_name=procedure_name)
            if not procedure:
                print(f"Procedure with name {procedure_name} does not exist.")
                return False
            assignment_exists = ProcedureRunModel.exists(
                id=self.id,
                procedure_id=procedure.id
            )
            return assignment_exists
        except Exception as e:
            print(f"Error checking if ProcedureRun belongs to Procedure: {e}")
            return False

    def unassociate_procedure(self):
        try:
            from gemini.api.procedure import Procedure
            procedure_run = ProcedureRunModel.get(self.id)
            if not procedure_run:
                print(f"ProcedureRun with ID {self.id} does not exist.")
                return None
            procedure = Procedure.get_by_id(procedure_run.procedure_id)
            procedure_run = ProcedureRunModel.update_parameter(
                procedure_run,
                "procedure_id",
                None
            )
            self.refresh()
            return procedure
        except Exception as e:
            print(f"Error unassociating Procedure from ProcedureRun: {e}")
            return None


    # def get_procedure(self):
    #     try:
    #         from gemini.api.procedure import Procedure
    #         current_id = self.id
    #         procedure_run_model = ProcedureRunsViewModel.get_by_parameters(
    #             procedure_run_id=current_id
    #         )
    #         procedure_id = procedure_run_model.procedure_id
    #         if not procedure_id:
    #             print(f"No procedure found for ProcedureRun with ID {current_id}.")
    #             return None
    #         procedure = Procedure.get_by_id(procedure_id)
    #         if not procedure:
    #             print(f"Procedure with ID {procedure_id} does not exist.")
    #             return None
    #         return procedure
    #     except Exception as e:
    #         print(f"Error getting Procedure for ProcedureRun: {e}")
    #         return None
            

    # def assign_procedure(self, procedure_name: str) -> Optional["ProcedureRun"]:
    #     try:
    #         from gemini.api.procedure import Procedure
    #         procedure = Procedure.get(procedure_name=procedure_name)
    #         if not procedure:
    #             print(f"Procedure with name {procedure_name} does not exist.")
    #             return None
    #         current_id = self.id
    #         assignment_exists = ProcedureRunModel.exists(
    #             id=current_id,
    #             procedure_id=procedure.id
    #         )
    #         if assignment_exists:
    #             print(f"ProcedureRun with ID {current_id} is already assigned to Procedure {procedure_name}.")
    #             return self
    #         db_procedure_run = ProcedureRunModel.update(
    #             db_procedure_run,
    #             procedure_id=procedure.id
    #         )
    #         procedure_run = self.model_validate(db_procedure_run)
    #         self.refresh()
    #         return procedure_run
    #     except Exception as e:
    #         print(f"Error assigning Procedure to ProcedureRun: {e}")
    #         return None

    # def unassign_procedure(self) -> Optional["ProcedureRun"]:
    #     try:
    #         current_id = self.id
    #         procedure_run = ProcedureRunModel.get(current_id)
    #         if not procedure_run:
    #             print(f"ProcedureRun with ID {current_id} does not exist.")
    #             return None
    #         db_procedure_run = ProcedureRunModel.update(
    #             procedure_run,
    #             procedure_id=None
    #         )
    #         procedure_run = self.model_validate(db_procedure_run)
    #         self.refresh()
    #         return procedure_run
    #     except Exception as e:
    #         print(f"Error unassigning Procedure from ProcedureRun: {e}")
    #         return None

    # def belongs_to_procedure(self, procedure_name: str) -> bool:
    #     try:
    #         from gemini.api.procedure import Procedure
    #         procedure = Procedure.get(procedure_name=procedure_name)
    #         if not procedure:
    #             print(f"Procedure with name {procedure_name} does not exist.")
    #             return False
    #         current_id = self.id
    #         assignment_exists = ProcedureRunModel.exists(
    #             id=current_id,
    #             procedure_id=procedure.id
    #         )
    #         if not assignment_exists:
    #             print(f"ProcedureRun with ID {current_id} is not assigned to Procedure {procedure_name}.")
    #             return False
    #         return True
    #     except Exception as e:
    #         print(f"Error checking if ProcedureRun belongs to Procedure: {e}")
    #         return False
    
        
            

   