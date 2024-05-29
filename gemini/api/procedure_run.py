from pydantic import BaseModel
from gemini.api.base import APIBase
from gemini.models import ProcedureModel, ProcedureRunModel
from gemini.logger import logger_service
from typing import Optional, List, Any, Union
from uuid import UUID

class ProcedureRun(APIBase):

    db_model = ProcedureRunModel

    procedure_id : Union[UUID, str]
    procedure_run_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        procedure_id: Union[UUID, str],
        procedure_run_info: dict = None
    ):
        
        db_instance = cls.db_model.get_or_create(
            procedure_id=procedure_id,
            procedure_run_info=procedure_run_info
        )
        instance = cls.model_validate(db_instance)
        logger_service.info(
            "API",
            f"Created a new instance of {cls.__name__} with id {instance.id}",
        )
        return instance
    

    @classmethod
    def get_procedure_runs(cls, procedure_id: Union[UUID, str]) -> List["ProcedureRun"]:
        db_instances = cls.db_model.get_by_parameters(procedure_id=procedure_id)
        instances = [cls.model_validate(db_instance) for db_instance in db_instances]
        logger_service.info("API", f"Retrieved procedure runs for procedure {procedure_id} from the database")
        return instances
    
    @classmethod
    def get(cls, procedure_run_id: str) -> "ProcedureRun":
        db_instance = cls.db_model.get_by_id(procedure_run_id)
        logger_service.info("API", f"Retrieved procedure run with id {procedure_run_id} from the database")
        return cls.model_validate(db_instance)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.id} from the database")
        return self.procedure_run_info
    
    def set_info(self, procedure_run_info: Optional[dict] = None) -> "ProcedureRun":
        self.update(procedure_run_info=procedure_run_info)
        logger_service.info("API", f"Set information about {self.id} in the database")
        return self
    
    def add_info(self, procedure_run_info: Optional[dict] = None) -> "ProcedureRun":
        current_info = self.get_info()
        updated_info = {**current_info, **procedure_run_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information to {self.id} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "ProcedureRun":
        current_info = self.get_info()
        updated_info = {k: v for k, v in current_info.items() if k not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info("API", f"Removed information from {self.id} in the database")
        return self
    