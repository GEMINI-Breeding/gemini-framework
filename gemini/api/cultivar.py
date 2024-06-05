from typing import Any, Optional, List
from gemini.api.base import APIBase
from gemini.models import CultivarModel, ExperimentModel, PlotViewModel
from gemini.logger import logger_service
from pydantic import computed_field


class Cultivar(APIBase):

    db_model = CultivarModel

    cultivar_population: str
    cultivar_accession: Optional[str] = None
    cultivar_info: Optional[dict] = None


    @classmethod
    def create(
        cls,
        cultivar_population: str,
        cultivar_accession: str = None,
        cultivar_info: dict = None,
        experiment_name: str = None,
    ):
        
        db_instance = cls.db_model.get_or_create(
            cultivar_population=cultivar_population,
            cultivar_accession=cultivar_accession,
            cultivar_info=cultivar_info
        )

        experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        experiment.cultivars.append(db_instance)
        experiment.save()
        
        logger_service.info("API", f"Created a new cultivar with accession {db_instance.cultivar_accession} in the database")
        
        return cls.model_validate(db_instance)
    
    @classmethod
    def get(cls, cultivar_population: str, cultivar_accession: str) -> "Cultivar":
        db_instance = cls.db_model.get_by_parameters(cultivar_population=cultivar_population, cultivar_accession=cultivar_accession)
        logger_service.info("API", f"Retrieved cultivar with accession {cultivar_accession} from the database")
        return cls.model_validate(db_instance) if db_instance else None
    
    @classmethod
    def get_population_accessions(cls, cultivar_population: str) -> List["Cultivar"]:
        cultivars = cls.db_model.search(cultivar_population=cultivar_population)
        cultivars = [cls.model_validate(cultivar) for cultivar in cultivars]
        logger_service.info("API", f"Retrieved {len(cultivars)} accessions of {cultivar_population} from the database")
        return cultivars if cultivars else None
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.cultivar_accession} from the database")
        return self.cultivar_info
    
    def set_info(self, cultivar_info: Optional[dict] = None) -> "Cultivar":
        self.update(cultivar_info=cultivar_info)
        logger_service.info("API", f"Set information about {self.cultivar_accession} in the database")
        return self
    
    def add_info(self, cultivar_info: dict) -> "Cultivar":
        current_info = self.get_info()
        updated_info = {**current_info, **cultivar_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information to {self.cultivar_accession} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Cultivar":
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info("API", f"Removed information from {self.cultivar_accession} in the database")
        return self
    

