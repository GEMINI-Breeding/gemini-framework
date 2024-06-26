from litestar.controller import Controller
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar import Response

from pydantic import BaseModel, UUID4
from datetime import datetime, date

from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.rest_api.src.models import (
    SeasonInput,
    SeasonOutput,
    SeasonSearch,
    SeasonBase
)

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
        
 