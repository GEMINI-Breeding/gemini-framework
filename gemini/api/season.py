from typing import List, Optional
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.db.models.seasons import SeasonModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.views.experiment_views import ExperimentSeasonsViewModel
from datetime import datetime, date, timedelta

class Season(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "season_id"))

    season_name: str
    season_start_date: date
    season_end_date: date
    season_info: Optional[dict] = None
    experiment_id: Optional[ID] = None

    def __str__(self):
        return f"Season(name={self.season_name}, start_date={self.season_start_date}, end_date={self.season_end_date})"
    
    def __repr__(self):
        return f"Season(id={self.id}, name={self.season_name}, start_date={self.season_start_date}, end_date={self.season_end_date})"

    @classmethod
    def exists(
        cls,
        season_name: str,
        experiment_name: str,
    ) -> bool:
        try:
            exists = ExperimentSeasonsViewModel.exists(
                season_name=season_name,
                experiment_name=experiment_name,
            )
            return exists
        except Exception as e:
            print(f"Error checking existence of season: {e}")
            return False
        
    @classmethod
    def create(
        cls,
        season_name: str,
        season_start_date: date = date.today(),
        season_end_date: date = date.today() + timedelta(days=30),
        season_info: dict = {},
        experiment_name: str = None
    ) -> Optional["Season"]:
        try:
            db_instance = SeasonModel.get_or_create(
                season_name=season_name,
                season_start_date=season_start_date,
                season_end_date=season_end_date,
                season_info=season_info,
            )
            season = cls.model_validate(db_instance)
            if experiment_name:
                season.associate_experiment(experiment_name=experiment_name)
            return season
        except Exception as e:
            print(f"Error creating season: {e}")
            return None
        
    @classmethod
    def get(
        cls,
        season_name: str,
        experiment_name: str = None
    ) -> Optional["Season"]:
        try:
            db_instance = ExperimentSeasonsViewModel.get_by_parameters(
                season_name=season_name,
                experiment_name=experiment_name,
            )
            if not db_instance:
                print(f"Season with name {season_name} does not exist.")
                return None
            season = cls.model_validate(db_instance)
            return season
        except Exception as e:
            print(f"Error retrieving season: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["Season"]:
        try:
            db_instance = SeasonModel.get(id)
            if not db_instance:
                print(f"Season with ID {id} does not exist.")
                return None
            season = cls.model_validate(db_instance)
            return season
        except Exception as e:
            print(f"Error retrieving season by ID: {e}")
            return None
        

    @classmethod
    def get_all(cls) -> Optional[List["Season"]]:
        try:
            seasons = SeasonModel.all()
            if not seasons or len(seasons) == 0:
                print("No seasons found.")
                return None
            seasons = [cls.model_validate(season) for season in seasons]
            return seasons
        except Exception as e:
            print(f"Error retrieving all seasons: {e}")
            return None
        
    @classmethod
    def search(
        cls, 
        season_name: str = None,
        experiment_name: str = None,
        season_start_date: datetime = None,
        season_end_date: datetime = None,
        season_info: dict = None
    ) -> Optional[List["Season"]]:
        try:
            if not any([season_name, experiment_name, season_start_date, season_end_date, season_info]):
                print("At least one search parameter must be provided.")
                return None
            seasons = ExperimentSeasonsViewModel.search(
                season_name=season_name,
                experiment_name=experiment_name,
                season_start_date=season_start_date,
                season_end_date=season_end_date,
                season_info=season_info
            )
            if not seasons or len(seasons) == 0:
                print("No seasons found matching the search criteria.")
                return None
            seasons = [cls.model_validate(season) for season in seasons]
            return seasons
        except Exception as e:
            print(f"Error searching for seasons: {e}")
            return None
        
    def update(
        self,
        season_name: str = None,
        season_start_date: date = None,
        season_end_date: date = None,
        season_info: dict = None
    ) -> Optional["Season"]:
        try:
            if not any([season_start_date, season_end_date, season_info, season_name]):
                print("At least one update parameter must be provided.")
                return None
            current_id = self.id
            season = SeasonModel.get(current_id)
            if not season:
                print(f"Season with ID {current_id} does not exist.")
                return None
            season = SeasonModel.update(
                season,
                season_name=season_name,
                season_start_date=season_start_date,
                season_end_date=season_end_date,
                season_info=season_info
            )
            updated_season = self.model_validate(season)
            self.refresh()  # Update the current instance
            return updated_season
        except Exception as e:
            print(f"Error updating season: {e}")
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            season = SeasonModel.get(current_id)
            if not season:
                print(f"Season with ID {current_id} does not exist.")
                return False
            SeasonModel.delete(season)
            return True
        except Exception as e:
            print(f"Error deleting season: {e}")
            return False
        
    def refresh(self) -> Optional["Season"]:
        try:
            db_instance = SeasonModel.get(self.id)
            if not db_instance:
                print(f"Season with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing season: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            season = SeasonModel.get(current_id)
            if not season:
                print(f"Season with ID {current_id} does not exist.")
                return None
            season_info = season.season_info
            if not season_info:
                print("Season info is empty.")
                return None
            return season_info
        except Exception as e:
            print(f"Error retrieving season info: {e}")
            return None
        
    def set_info(self, season_info: dict) -> Optional["Season"]:
        try:
            current_id = self.id
            season = SeasonModel.get(current_id)
            if not season:
                print(f"Season with ID {current_id} does not exist.")
                return None
            season = SeasonModel.update(
                season,
                season_info=season_info
            )
            updated_season = self.model_validate(season)
            self.refresh()  # Update the current instance
            return updated_season
        except Exception as e:
            print(f"Error setting season info: {e}")
            return None
        
    def get_associated_experiment(self):
        try:
            from gemini.api.experiment import Experiment
            if not self.experiment_id:
                print("This season is not assigned to any experiment.")
                return None
            experiment = Experiment.get_by_id(self.experiment_id)
            if not experiment:
                print(f"Experiment with ID {self.experiment_id} does not exist.")
                return None
            return experiment
        except Exception as e:
            print(f"Error retrieving experiment for season: {e}")
            return None

    def associate_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment with name {experiment_name} does not exist.")
                return None
            existing_association = ExperimentSeasonsViewModel.exists(
                season_id=self.id,
                experiment_id=experiment.id
            )
            if existing_association:
                print(f"Season {self.season_name} is already assigned to experiment {experiment_name}.")
                return self
            db_season = SeasonModel.get(self.id)
            db_season = SeasonModel.update(
                db_season,
                experiment_id=experiment.id
            )
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error assigning experiment to season: {e}")
            return None

    def unassociate_experiment(self):
        try:
            from gemini.api.experiment import Experiment
            if not self.experiment_id:
                print("This season is not assigned to any experiment.")
                return None
            db_season = SeasonModel.get(self.id)
            if not db_season:
                print(f"Season with ID {self.id} does not exist.")
                return None
            experiment = Experiment.get_by_id(self.experiment_id)
            db_season = SeasonModel.update(
                db_season,
                experiment_id=None
            )
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error unassigning experiment from season: {e}")
            return None

    def belongs_to_experiment(self, experiment_name: str) -> bool:
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment with name {experiment_name} does not exist.")
                return False
            association_exists = ExperimentSeasonsViewModel.exists(
                season_id=self.id,
                experiment_id=experiment.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking if season belongs to experiment: {e}")
            return False

