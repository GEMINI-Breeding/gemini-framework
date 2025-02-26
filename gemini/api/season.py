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

            if experiment_name:
                db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
                if db_experiment:
                    SeasonModel.update(db_instance, experiment_id=db_experiment.id)
            
            season = cls.model_validate(db_instance)
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
            season = cls.model_validate(db_instance)
            return season
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Season":
        try:
            db_instance = SeasonModel.get(id)
            season = cls.model_validate(db_instance)
            return season
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["Season"]:
        try:
            seasons = SeasonModel.all()
            seasons = [cls.model_validate(season) for season in seasons]
            return seasons
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
            if any([experiment_name, season_name, season_start_date, season_end_date, season_info]):
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
        season_start_date: date = None,
        season_end_date: date = None,
        season_info: dict = None
    ) -> "Season":
        try:
            if any([season_start_date, season_end_date, season_info]):
                raise Exception("At least one update parameter must be provided.")
            current_id = self.id
            season = SeasonModel.get(current_id)
            season = SeasonModel.update(
                season,
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
        
    

    
        

        

        
