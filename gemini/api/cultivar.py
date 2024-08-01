from typing import Any, Optional, List
from gemini.api.base import APIBase, ID
from gemini.server.database.models import CultivarModel, ExperimentModel, ExperimentCultivarsViewModel
from pydantic import Field, AliasChoices


class Cultivar(APIBase):
    """
    Represents a cultivar in the system.
    """

    db_model = CultivarModel

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "cultivar_id"))
    cultivar_population: str
    cultivar_accession: Optional[str] = None
    cultivar_info: Optional[dict] = None


    @classmethod
    def create(
        cls,
        cultivar_population: str ='Default',
        cultivar_accession: str = 'Default',
        cultivar_info: dict = {},
        experiment_name: str = 'Default'
    ):
        """
        Creates a new cultivar.

        Args:
            cultivar_population (str): The population of the cultivar.
            cultivar_accession (str): The accession of the cultivar.
            cultivar_info (dict): Additional information about the cultivar.
            experiment_name (str): The name of the experiment.

        Returns:
            Cultivar: The created cultivar instance.
        """
        
        db_instance = cls.db_model.get_or_create(
            cultivar_population=cultivar_population,
            cultivar_accession=cultivar_accession,
            cultivar_info=cultivar_info
        )

        experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        experiment.cultivars.append(db_instance)
        experiment.save()
        
        return cls.model_validate(db_instance)
    
    @classmethod
    def get(cls, cultivar_population: str, cultivar_accession: str) -> "Cultivar":
        """
        Retrieves a cultivar by its population and accession.

        Args:
            cultivar_population (str): The population of the cultivar.
            cultivar_accession (str): The accession of the cultivar.

        Returns:
            Cultivar: The retrieved cultivar instance, or None if not found.
        """
        db_instance = cls.db_model.get_by_parameters(cultivar_population=cultivar_population, cultivar_accession=cultivar_accession)
        return cls.model_validate(db_instance) if db_instance else None
    
    @classmethod
    def get_population_accessions(cls, cultivar_population: str) -> List["Cultivar"]:
        """
        Retrieves all cultivars in a given population.

        Args:
            cultivar_population (str): The population of the cultivars.

        Returns:
            List[Cultivar]: A list of cultivar instances in the population, or None if not found.
        """
        cultivars = cls.db_model.search(cultivar_population=cultivar_population)
        cultivars = [cls.model_validate(cultivar) for cultivar in cultivars]
        return cultivars if cultivars else None
    
    def get_info(self) -> dict:
        """
        Retrieves the information of the cultivar.

        Returns:
            dict: The information of the cultivar.
        """
        self.refresh()
        return self.cultivar_info
    
    def set_info(self, cultivar_info: Optional[dict] = None) -> "Cultivar":
        """
        Sets the information of the cultivar.

        Args:
            cultivar_info (dict): The information to set for the cultivar.

        Returns:
            Cultivar: The updated cultivar instance.
        """
        self.update(cultivar_info=cultivar_info)
        return self
    
    def add_info(self, cultivar_info: dict) -> "Cultivar":
        """
        Adds additional information to the cultivar.

        Args:
            cultivar_info (dict): The additional information to add.

        Returns:
            Cultivar: The updated cultivar instance.
        """
        current_info = self.get_info()
        updated_info = {**current_info, **cultivar_info}
        self.set_info(updated_info)
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Cultivar":
        """
        Removes specific keys from the cultivar information.

        Args:
            keys_to_remove (List[str]): The keys to remove from the cultivar information.

        Returns:
            Cultivar: The updated cultivar instance.
        """
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        return self
    
    @classmethod
    def search(cls,
        experiment_name: str = None,
        **search_parameters: Any
    ) -> List["Cultivar"]:
        """
        Searches for cultivars based on the given parameters.

        Args:
            experiment_name (str): The name of the experiment to filter by.
            **search_parameters (Any): Additional search parameters.

        Returns:
            List[Cultivar]: A list of cultivar instances matching the search criteria, or None if not found.
        """
        cultivars = ExperimentCultivarsViewModel.search(
            experiment_name=experiment_name,
            **search_parameters
        )
        cultivars = [cls.model_validate(cultivar) for cultivar in cultivars]
        return cultivars if cultivars else None
   
        
    

