from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.db.models.cultivars import CultivarModel
from gemini.db.models.associations import ExperimentCultivarModel
from gemini.db.models.views.experiment_views import ExperimentCultivarsViewModel

class Cultivar(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "cultivar_id"))

    cultivar_population: str
    cultivar_accession: Optional[str] = None
    cultivar_info: Optional[dict] = None

    @classmethod
    def exists(
        cls,
        cultivar_population: str,
        cultivar_accession: str
    ) -> bool:
        try:
            exists = CultivarModel.exists(
                cultivar_population=cultivar_population,
                cultivar_accession=cultivar_accession
            )
            return exists
        except Exception as e:
            raise e

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
            cultivar = cls.model_validate(db_instance)
            if experiment_name:
                cultivar.assign_experiment(experiment_name=experiment_name)
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
            cultivar = cls.model_validate(db_instance) if db_instance else None
            return cultivar
        except Exception as e:
            raise e
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Cultivar":
        try:
            db_instance = CultivarModel.get(id)
            cultivar = cls.model_validate(db_instance) if db_instance else None
            return cultivar
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
        
    def get_info(self) -> dict:
        try:
            current_id = self.id
            cultivar = CultivarModel.get(current_id)
            cultivar_info = cultivar.cultivar_info
            if not cultivar_info:
                raise Exception("Cultivar info is empty.")
            return cultivar_info
        except Exception as e:
            raise e
        
    def set_info(self, cultivar_info: dict) -> "Cultivar":
        try:
            current_id = self.id
            cultivar = CultivarModel.get(current_id)
            cultivar = CultivarModel.update(cultivar, cultivar_info=cultivar_info)
            cultivar = self.model_validate(cultivar)
            self.refresh()
            return cultivar
        except Exception as e:
            raise e
    
    def get_plots():
        pass

    def assign_plot():
        pass

    def belongs_to_plot():
        pass

    def unassign_plot():
        pass

    def get_experiments(self):
        try:
            from gemini.api.experiment import Experiment
            db_instance = CultivarModel.get(self.id)
            experiments = ExperimentCultivarsViewModel.search(cultivar_id=db_instance.id)
            experiments = [Experiment.model_validate(experiment) for experiment in experiments]
            return experiments if experiments else None
        except Exception as e:
            raise e

    def assign_experiment(self, experiment_name: str) -> bool:
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                raise Exception(f"Experiment {experiment_name} does not exist.")
            if experiment.has_cultivar(cultivar_accession=self.cultivar_accession, cultivar_population=self.cultivar_population):
                print(f"Cultivar {self.cultivar_accession} and {self.cultivar_population} already assigned to experiment {experiment_name}.")
                return True
            ExperimentCultivarModel.get_or_create(
                experiment_id=experiment.id,
                cultivar_id=self.id
            )
            return True
        except Exception as e:
            return False


    def belongs_to_experiment(self, experiment_name: str) -> bool:
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                raise Exception(f"Experiment {experiment_name} does not exist.")
            belongs = experiment.has_cultivar(
                cultivar_accession=self.cultivar_accession,
                cultivar_population=self.cultivar_population
            )
            return belongs
        except Exception as e:
            return False

    def unassign_experiment(self, experiment_name: str) -> bool:
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                raise Exception(f"Experiment {experiment_name} does not exist.")
            if not experiment.has_cultivar(
                cultivar_accession=self.cultivar_accession,
                cultivar_population=self.cultivar_population
            ):
                print(f"Cultivar {self.cultivar_accession} and {self.cultivar_population} not assigned to experiment {experiment_name}.")
                return False
            experiment_cultivar_instance = ExperimentCultivarModel.get_by_parameters(
                experiment_id=experiment.id,
                cultivar_id=self.id
            )
            if not experiment_cultivar_instance:
                raise Exception(f"Cultivar {self.cultivar_accession} and {self.cultivar_population} not assigned to experiment {experiment_name}.")
            is_deleted = ExperimentCultivarModel.delete(experiment_cultivar_instance)
            return is_deleted
        except Exception as e:
            return False
        
    @classmethod
    def get_population_accessions(cls, cultivar_population: str) -> List["Cultivar"]:
        try:
            cultivars = CultivarModel.search(cultivar_population=cultivar_population)
            cultivars = [cls.model_validate(cultivar) for cultivar in cultivars]
            return cultivars if cultivars else None
        except Exception as e:
            raise e
        

 