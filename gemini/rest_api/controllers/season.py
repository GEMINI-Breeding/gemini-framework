from litestar.controller import Controller
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar import Response

from pydantic import BaseModel, UUID4
from datetime import datetime, date

from gemini.api.experiment import Experiment
from gemini.api.season import Season

from typing import List, Annotated, Optional

class SeasonInput(BaseModel):
    season_name: str = "2023"
    experiment_name: str = "Test Experiment"
    season_info: Optional[dict] = {}
    season_start_date: Optional[date] = datetime.now().date()
    season_end_date: Optional[date] = datetime.now().date()
    

class SeasonController(Controller):
    
    # Get Seasons
    @get()
    async def get_seasons(
        self,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        season_start_date: Optional[date] = None,
        season_end_date: Optional[date] = None,
        season_info: Optional[dict] = None
    ) -> List[Season]:
        experiment = Experiment.get(experiment_name=experiment_name)
        seasons = Season.search(
            experiment_id=experiment.id,
            season_name=season_name,
            season_start_date=season_start_date,
            season_end_date=season_end_date,
            season_info=season_info
        )
        if seasons is None:
            return Response(status_code=404)
        return seasons
    
    # Get by experiment name and season name
    @get('/{season_name:str}/experiment/{experiment_name:str}')
    async def get_season(
        self,
        experiment_name: str,
        season_name: str
    ) -> Season:
        season = Season.get(experiment_name=experiment_name, season_name=season_name)
        if season is None:
            return Response(status_code=404)
        return season
    
    # Get season Info
    @get('/{season_name:str}/experiment/{experiment_name:str}/info')
    async def get_season_info(
        self,
        experiment_name: str,
        season_name: str
    ) -> dict:
        season = Season.get(experiment_name=experiment_name, season_name=season_name)
        if season is None:
            return Response(status_code=404)
        return season.get_info()
    
    # Set season Info
    @patch('/{season_name:str}/experiment/{experiment_name:str}/info')
    async def set_season_info(
        self,
        experiment_name: str,
        season_name: str,
        data: dict
    ) -> dict:
        season = Season.get(experiment_name=experiment_name, season_name=season_name)
        if season is None:
            return Response(status_code=404)
        season.set_info(season_info=data)
        return season.get_info()