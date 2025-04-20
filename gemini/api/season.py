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
            raise e
        
    def get_experiment(self):
        try:
            from gemini.api.experiment import Experiment
            if not self.experiment_id:
                return None
            
            experiment = Experiment.get_by_id(self.experiment_id)
            if not experiment:
                raise Exception(f"Experiment with ID {self.experiment_id} does not exist.")
            return experiment
        except Exception as e:
            raise e

    def assign_experiment(self, experiment_name: str) -> bool:
        try:
            from gemini.api.experiment import Experiment
            
            if self.experiment_id:
                current_experiment = Experiment.get_by_id(self.experiment_id)
                if current_experiment and current_experiment.experiment_name != experiment_name:
                    print(f"Season {self.season_name} is already assigned to experiment {current_experiment.experiment_name}. Cannot reassign.")
                    return False
                elif current_experiment and current_experiment.experiment_name == experiment_name:
                     print(f"Season {self.season_name} is already assigned to experiment {experiment_name}.")
                     return True # Already assigned to the correct one

            # Get the target experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                raise Exception(f"Experiment {experiment_name} does not exist.")

            # Update the season's experiment_id
            db_instance = SeasonModel.get(self.id)
            SeasonModel.update(db_instance, experiment_id=experiment.id)
            self.refresh() # Update the current instance
            return True
        except Exception as e:
            print(f"Error assigning experiment: {e}")
            return False

    @classmethod
    def create(
        cls,
        season_name: str,
        season_start_date: date = date.today(),
        season_end_date: date = date.today() + timedelta(days=30),
        season_info: dict = {},
        experiment_name: str = None
    ) -> "Season":
        try:
            db_instance = SeasonModel.get_or_create(
                season_name=season_name,
                season_start_date=season_start_date,
                season_end_date=season_end_date,
                season_info=season_info,
            )

            season = cls.model_validate(db_instance)
            if experiment_name:
                season.assign_experiment(experiment_name)
            return season
        except Exception as e:
            raise e


    @classmethod
    def get(cls, season_name: str, experiment_name: str) -> "Season":
        try:
            experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
            db_instance = SeasonModel.get_by_parameters(
                season_name=season_name,
                experiment_id=experiment.id if experiment else None,
            )
            season = cls.model_validate(db_instance) if db_instance else None
            return season
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Season":
        try:
            db_instance = SeasonModel.get(id)
            season = cls.model_validate(db_instance) if db_instance else None
            return season
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["Season"]:
        try:
            seasons = SeasonModel.all()
            seasons = [cls.model_validate(season) for season in seasons]
            return seasons if seasons else None
        except Exception as e:
            raise e
        
    @classmethod
    def search(
        cls, 
        experiment_name: str = None,
        season_name: str = None,
        season_start_date: datetime = None,
        season_end_date: datetime = None,
        season_info: dict = None
    ) -> List["Season"]:
        try:
            if not any([experiment_name, season_name, season_start_date, season_end_date, season_info]):
                raise Exception("At least one search parameter must be provided.")

            seasons = ExperimentSeasonsViewModel.search(
                experiment_name=experiment_name,
                season_name=season_name,
                season_start_date=season_start_date,
                season_end_date=season_end_date,
                season_info=season_info
            )
            seasons = [cls.model_validate(season) for season in seasons]
            return seasons if seasons else None
        except Exception as e:
            raise e
        
    def update(
        self,
        season_name: str = None,
        season_start_date: date = None,
        season_end_date: date = None,
        season_info: dict = None
    ) -> "Season":
        try:
            if not any([season_start_date, season_end_date, season_info, season_name]):
                raise Exception("At least one update parameter must be provided.")
            current_id = self.id
            season = SeasonModel.get(current_id)
            season = SeasonModel.update(
                season,
                season_name=season_name,
                season_start_date=season_start_date,
                season_end_date=season_end_date,
                season_info=season_info
            )
            season = self.model_validate(season)
            self.refresh()
            return season
        except Exception as e:
            raise e


    def delete(self) -> bool:
        try:
            current_id = self.id
            season = SeasonModel.get(current_id)
            SeasonModel.delete(season)
            return True
        except Exception as e:
            raise e
    
    def refresh(self) -> "Season":
        try:
            db_instance = SeasonModel.get(self.id)
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
            season = SeasonModel.get(current_id)
            season_info = season.season_info
            if not season_info:
                raise Exception("Season info is empty.")
            return season_info
        except Exception as e:
            raise e
        
    def set_info(self, season_info: dict) -> "Season":
        try:
            current_id = self.id
            season = SeasonModel.get(current_id)
            season = SeasonModel.update(
                season,
                season_info=season_info
            )
            season = self.model_validate(season)
            self.refresh()
            return self
        except Exception as e:
            raise e
