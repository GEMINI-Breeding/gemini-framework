from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.db.models.cultivars import CultivarModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.associations import ExperimentCultivarModel
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
        experiment_name: str = None
    ) -> "Cultivar":
        try:
            db_instance = CultivarModel.get_or_create(
                cultivar_population=cultivar_population,
                cultivar_accession=cultivar_accession,
                cultivar_info=cultivar_info,
            )
            if experiment_name:
                db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
                if db_experiment:
                    ExperimentCultivarModel.get_or_create(experiment_id=db_experiment.id, cultivar_id=db_instance.id)
            cultivar = cls.model_validate(db_instance)
            return cultivar

        except Exception as e:
            raise e
        

    @classmethod
    def get(cls, cultivar_population: str, cultivar_accession: str, experiment_name: str = None) -> "Cultivar":
        try:
            db_instance = ExperimentCultivarsViewModel.get_by_parameters(
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population,
                experiment_name=experiment_name,
            )
            cultivar = cls.model_validate(db_instance)
            return cultivar if cultivar else None
        except Exception as e:
            raise e
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Cultivar":
        try:
            db_instance = CultivarModel.get(id)
            cultivar = cls.model_validate(db_instance)
            return cultivar if cultivar else None
        except Exception as e:
            raise e
        
    @classmethod
    def get_all(cls) -> List["Cultivar"]:
        try:
            cultivars = CultivarModel.all()
            cultivars = [cls.model_validate(cultivar) for cultivar in cultivars]
            return cultivars if cultivars else None
        except Exception as e:
            raise e
        
    @classmethod
    def search(
        cls, 
        experiment_name: str = None,
        cultivar_population: str = None,
        cultivar_accession: str = None,
        cultivar_info: dict = None
    ) -> List["Cultivar"]:
        try:

            if not experiment_name and not cultivar_population and not cultivar_accession and not cultivar_info:
                raise Exception("At least one search parameter must be provided.")

            cultivars = ExperimentCultivarsViewModel.search(
                experiment_name=experiment_name,
                cultivar_population=cultivar_population,
                cultivar_accession=cultivar_accession,
                cultivar_info=cultivar_info,
            )
            cultivars = [cls.model_validate(cultivar) for cultivar in cultivars]
            return cultivars if cultivars else None
        except Exception as e:
            raise e
        
    def update(
        self,
        cultivar_accession: str = None,
        cultivar_population: str = None,
        cultivar_info: dict = None,
    ) -> "Cultivar":
        try:

            if not cultivar_accession and not cultivar_population and not cultivar_info:
                raise ValueError("At least one parameter must be provided.")

            current_id = self.id
            cultivar = CultivarModel.get(current_id)
            cultivar = CultivarModel.update(
                cultivar,
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population,
                cultivar_info=cultivar_info,
            )
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
        
    
    def refresh(self) -> "Cultivar":
        try:
            db_instance = CultivarModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e
    
        
    @classmethod
    def get_population_accessions(cls, cultivar_population: str) -> List["Cultivar"]:
        try:
            cultivars = CultivarModel.search(cultivar_population=cultivar_population)
            cultivars = [cls.model_validate(cultivar) for cultivar in cultivars]
            return cultivars if cultivars else None
        except Exception as e:
            raise e
        

 