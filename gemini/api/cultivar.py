from typing import Optional
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.db.models.cultivars import CultivarModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.views.experiment_views import ExperimentCultivarsViewModel

class Cultivar(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "cultivar_id"))

    cultivar_population: str
    cultivar_accession: Optional[str] = None
    cultivar_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        cultivar_population: str,
        cultivar_accession: str,
        cultivar_info: dict = {},
        experiment_name: str = "Default", 
    ) -> "Cultivar":
        try:
            db_instance = CultivarModel.get_or_create(
                cultivar_population=cultivar_population,
                cultivar_accession=cultivar_accession,
                cultivar_info=cultivar_info,
            )
            cultivar = cls.model_validate(db_instance)
            experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
            if experiment:
                experiment.cultivars.append(cultivar)
            return cultivar
        except Exception as e:
            raise e
        

    @classmethod
    def get(cls, cultivar_population: str, cultivar_accession: str) -> "Cultivar":
        try:
            db_instance = CultivarModel.get_by_parameters(
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population,
            )
            cultivar = cls.model_validate(db_instance)
            return cultivar
        except Exception as e:
            raise e
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Cultivar":
        try:
            db_instance = CultivarModel.get(id)
            cultivar = cls.model_validate(db_instance)
            return cultivar
        except Exception as e:
            raise e
        
    @classmethod
    def get_all(cls) -> list["Cultivar"]:
        try:
            cultivars = CultivarModel.all()
            cultivars = [cls.model_validate(cultivar) for cultivar in cultivars]
            return cultivars if cultivars else None
        except Exception as e:
            raise e
        
    @classmethod
    def search(cls, **search_parameters) -> list["Cultivar"]:
        try:
            cultivars = ExperimentCultivarsViewModel.search(**search_parameters)
            cultivars = [cls.model_validate(cultivar) for cultivar in cultivars]
            return cultivars if cultivars else None
        except Exception as e:
            raise e
        
    def update(self, **update_parameters) -> "Cultivar":
        try:
            current_id = self.id
            cultivar = CultivarModel.get(current_id)
            cultivar = CultivarModel.update(cultivar, **update_parameters)
            cultivar = self.model_validate(cultivar)
            self.refresh()
            return cultivar
        except Exception as e:
            raise e
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            cultivar = CultivarModel.get(current_id)
            CultivarModel.delete(cultivar)
            return True
        except Exception as e:
            return False
        
    
    def refresh(self):
        try:
            db_instance = CultivarModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    actual_value = getattr(instance, key)
                    setattr(self, key, actual_value)
            return self
        except Exception as e:
            raise e
    
        
    @classmethod
    def get_population_accessions(cls, cultivar_population: str):
        cultivars = CultivarModel.search(cultivar_population=cultivar_population)
        cultivars = [cls.model_validate(cultivar) for cultivar in cultivars]
        return cultivars if cultivars else None
    

 