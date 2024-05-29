from typing import List, Optional, Any
from gemini.api.base import APIBase
from gemini.api.dataset import Dataset
from gemini.api.model_run import ModelRun
from gemini.models import ModelModel
from gemini.logger import logger_service
from typing import List, Optional, Any


class Model(APIBase):

    db_model = ModelModel

    model_name: str
    model_url: Optional[str] = None
    model_info: Optional[dict] = None

    datasets: Optional[List[Dataset]] = None
    model_runs: Optional[List[ModelRun]] = None

    @classmethod
    def create(
        cls,
        model_name: str,
        model_url: str = None,
        model_info: dict = None
    ):
        db_instance = ModelModel.get_or_create(
            model_name=model_name,
            model_url=model_url,
            model_info=model_info
        )
        instance = cls.model_validate(db_instance)
        logger_service.info(
            "API",
            f"Created a new instance of {cls.__name__} with id {instance.id}",
        )
        return instance
    
    @classmethod
    def get(cls, model_name: str) -> "Model":
        db_instance = ModelModel.get_by_parameters(model_name=model_name)
        logger_service.info("API", f"Retrieved model with name {model_name} from the database")
        return cls.model_validate(db_instance)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.model_name} from the database")
        return self.model_info
    
    def set_info(self, model_info: Optional[dict] = None) -> "Model":
        self.update(model_info=model_info)
        logger_service.info("API", f"Set information about {self.model_name} in the database")
        return self
    
    def add_info(self, model_info: Optional[dict] = None) -> "Model":
        current_info = self.get_info()
        updated_info = {**current_info, **model_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information to {self.model_name} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Model":
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info("API", f"Removed information from {self.model_name} in the database")
        return self
    
    def get_datasets(self) -> List[Dataset]:
        self.refresh()
        logger_service.info("API", f"Retrieved datasets for model {self.model_name} from the database")
        return self.datasets
    
    def get_model_runs(self) -> List[ModelRun]:
        self.refresh()
        logger_service.info("API", f"Retrieved model runs for model {self.model_name} from the database")
        return self.model_runs

    # Todo: Add and remove datasets
    # Todo: Add and remove records
    # Todo: Add and remove model runs
