from litestar.controller import Controller
from litestar import Response
from litestar.handlers import get, patch, post
from litestar.params import Body
from datetime import date

from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.server.rest_api.src.models import (
    SeasonOutput,
    SeasonInput
)

from typing import List, Annotated, Optional


class SeasonController(Controller):
    
    # Get Seasons
    @get()
    async def get_seasons(
        self,
        season_name: Optional[str] = None,
        season_start_date: Optional[date] = None,
        season_end_date: Optional[date] = None,
        season_info: Optional[dict] = None,
        experiment_name: Optional[str] = 'Default'
    ) -> List[SeasonOutput]:
        try:
            experiment = Experiment.get(experiment_name=experiment_name)
            seasons = Season.search(
                experiment_id=experiment.id,
                season_name=season_name,
                season_start_date=season_start_date,
                season_end_date=season_end_date,
                season_info=season_info
            )
            if seasons is None:
                return Response(content="No seasons found", status_code=404)
            seasons = [season.model_dump() for season in seasons]
            seasons = [SeasonOutput.model_validate(season) for season in seasons]
            return seasons
        except Exception as e:
            return Response(content=str(e), status_code=500)
    
    # Create Season
    @post()
    async def create_season(
        self,
        data: Annotated[SeasonInput, Body]
    ) -> SeasonOutput:
        try:
            experiment = Experiment.get(experiment_name=data.experiment_name)
            season = Season.create(
                season_name=data.season_name,
                season_info=data.season_info,
                season_start_date=data.season_start_date,
                season_end_date=data.season_end_date,
                experiment_name=experiment.experiment_name
            )
            return SeasonOutput.model_validate(season.model_dump())
        except Exception as e:
            return Response(content=str(e), status_code=500)



    # Get Season by ID
    @get(path="/id/{season_id:str}")
    async def get_season_by_id(
        self, season_id: str
    ) -> SeasonOutput:
        try:
            season = Season.get_by_id(id=season_id)
            if season is None:
                return Response(content="Season not found", status_code=404)
            season = SeasonOutput.model_validate(season.model_dump())
            return season
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Season Info by Season and Experiment
    @get('/{season_name:str}/experiment/{experiment_name:str}/info')
    async def get_season_info(
        self,
        experiment_name: str,
        season_name: str
    ) -> dict:
        try:
            season = Season.get(experiment_name=experiment_name, season_name=season_name)
            if season is None:
                return Response(content="Season not found", status_code=404)
            return season.get_info()
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Set Season Info by Season and Experiment
    @patch('/{season_name:str}/experiment/{experiment_name:str}/info')
    async def set_season_info(
        self,
        experiment_name: str,
        season_name: str,
        data: dict
    ) -> dict:
        try:
            season = Season.get(experiment_name=experiment_name, season_name=season_name)
            if season is None:
                return Response(content="Season not found", status_code=404)
            season.set_info(season_info=data)
            return season.get_info()
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
 