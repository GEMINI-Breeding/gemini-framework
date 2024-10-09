from typing import Optional, List, Any, Union
from gemini.api.base import APIBase, ID
from gemini.server.database.models import SeasonModel, ExperimentModel
from datetime import datetime, date
from uuid import UUID
from pydantic import Field, AliasChoices


class Season(APIBase):
    """
    Represents a season in the Gemini framework.

    Attributes:
        db_model (Type): The database model associated with the season.
        id (Optional[ID]): The ID of the season.
        season_name (str): The name of the season.
        season_info (Optional[dict]): Additional information about the season.
        season_start_date (Optional[date]): The start date of the season.
        season_end_date (Optional[date]): The end date of the season.
        experiment_id (Optional[Union[str, UUID]]): The ID of the experiment associated with the season.

    Methods:
        get(experiment_name: str, season_name: str) -> Season:
            Retrieves a season by its experiment name and season name.
        get_by_experiment(experiment_name: str) -> List[Season]:
            Retrieves all seasons associated with a specific experiment.
        get_info() -> dict:
            Retrieves the additional information about the season.
        set_info(season_info: Optional[dict] = None) -> Season:
            Sets the additional information for the season.
        add_info(season_info: Optional[dict] = None) -> Season:
            Adds additional information to the existing season information.
        remove_info(keys_to_remove: List[str]) -> Season:
            Removes specific keys from the existing season information.
    """
    db_model = SeasonModel

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "season_id"))
    season_name: str
    season_info: Optional[dict] = None
    season_start_date: Optional[date] = None
    season_end_date: Optional[date] = None
    experiment_id: Optional[Union[str, UUID]] = None

    @classmethod
    def create(
        cls,
        season_name: str = 'Default',
        season_info: Optional[dict] = None,
        season_start_date: Optional[date] = None,
        season_end_date: Optional[date] = None,
        experiment_name: str = 'Default'
    ):
        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        db_instance = SeasonModel.get_or_create(
            season_name=season_name,
            season_info=season_info,
            season_start_date=season_start_date,
            season_end_date=season_end_date,
            experiment_id=db_experiment.id
        )
        return cls.model_validate(db_instance)
    

    @classmethod
    def get(cls, experiment_name: str, season_name: str) -> "Season":
        """
        Retrieves a season by its experiment name and season name.

        Args:
            experiment_name (str): The name of the experiment.
            season_name (str): The name of the season.

        Returns:
            Season: The retrieved season.

        Raises:
            SomeException: If the season cannot be found.
        """
        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        db_instance = SeasonModel.get_by_parameters(experiment_id=db_experiment.id, season_name=season_name)
        return cls.model_validate(db_instance)
    
    @classmethod
    def get_by_experiment(cls, experiment_name: str) -> List["Season"]:
        """
        Retrieves all seasons associated with a specific experiment.

        Args:
            experiment_name (str): The name of the experiment.

        Returns:
            List[Season]: A list of seasons associated with the experiment.

        Raises:
            SomeException: If the experiment cannot be found.
        """
        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        db_instances = SeasonModel.search(experiment_id=db_experiment.id)
        return [cls.model_validate(db_instance) for db_instance in db_instances]

    def get_info(self) -> dict:
        """
        Retrieves the additional information about the season.

        Returns:
            dict: The additional information about the season.
        """
        self.refresh()
        return self.season_info
    
    def set_info(self, season_info: Optional[dict] = None) -> "Season":
        """
        Sets the additional information for the season.

        Args:
            season_info (Optional[dict]): The additional information to set for the season.

        Returns:
            Season: The updated season.
        """
        self.update(season_info=season_info)
        return self
    
    def add_info(self, season_info: Optional[dict] = None) -> "Season":
        """
        Adds additional information to the existing season information.

        Args:
            season_info (Optional[dict]): The additional information to add to the existing season information.

        Returns:
            Season: The updated season.
        """
        current_info = self.get_info()
        updated_info = {**current_info, **season_info}
        self.set_info(updated_info)
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Season":
        """
        Removes specific keys from the existing season information.

        Args:
            keys_to_remove (List[str]): The keys to remove from the existing season information.

        Returns:
            Season: The updated season.
        """
        current_info = self.get_info()
        updated_info = {k: v for k, v in current_info.items() if k not in keys_to_remove}
        self.set_info(updated_info)
        return self
        
