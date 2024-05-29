from collections.abc import AsyncGenerator
from datetime import datetime, date
from typing import Annotated, List, Optional
from uuid import UUID

from litestar import Request
from litestar.controller import Controller
from litestar.dto import DTOConfig, DTOData
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import delete, get, patch, post
from litestar.params import Body
from litestar.response import Stream
from litestar.serialization import default_serializer, encode_json
from pydantic import BaseModel

from gemini.api.season import Season
from gemini.api.experiment import Experiment
from gemini.api.plot import Plot


class SeasonInput(BaseModel):
    season_name: str
    season_info: Optional[dict] = {}
    season_start_date: Optional[date] = datetime.now().date()
    season_end_date: Optional[date] = datetime.now().date()
    experiment_name: Optional[str] = None


class SeasonController(Controller):

    # Filter seasons
    @get()
    async def get_seasons(
        self,
        season_name: Optional[str] = None,
        season_start_date: Optional[date] = None,
        season_end_date: Optional[date] = None,
        season_info: Optional[dict] = None,
    ) -> List[Season]:
        seasons = Season.search(
            season_name=season_name,
            season_start_date=season_start_date,
            season_end_date=season_end_date,
            season_info=season_info,
        )
        return seasons

    # Get Season by ID
    @get(path="/id/{season_id:uuid}")
    async def get_season_by_id(self, season_id: UUID) -> Season:
        season = Season.get_by_id(season_id)
        return season

    # Create a new season
    @post()
    async def create_season(self, season_input: Annotated[SeasonInput, Body]) -> Season:
        season = Season.create(
            season_name=season_input.season_name,
            season_info=season_input.season_info,
            season_start_date=season_input.season_start_date,
            season_end_date=season_input.season_end_date,
            experiment_name=season_input.experiment_name,
        )
        return season

    # Get Seasons by Experiment Name
    @get(path="/experiment/{experiment_name:str}")
    async def get_seasons_by_experiment(self, experiment_name: str) -> List[Season]:
        seasons = Season.get_by_experiment(experiment_name=experiment_name)
        return seasons

    # Get Season by Experiment and Season Name
    @get(path="/experiment/{experiment_name:str}/{season_name:str}")
    async def get_season_by_experiment_season(
        self, experiment_name: str, season_name: str
    ) -> Season:
        season = Season.get_by_experiment_season(
            experiment_name=experiment_name, season_name=season_name
        )
        return season

    # Get Season Info by Experiment and Season Name
    @get(path="/experiment/{experiment_name:str}/{season_name:str}/info")
    async def get_season_info(self, experiment_name: str, season_name: str) -> dict:
        season = Season.get_by_experiment_season(
            experiment_name=experiment_name, season_name=season_name
        )
        season = season.get_info()
        return season

    # Set Season Info by Experiment and Season Name
    @patch(path="/experiment/{experiment_name:str}/{season_name:str}/info")
    async def set_season_info(
        self, experiment_name: str, season_name: str, info: Annotated[dict, Body]
    ) -> Season:
        season = Season.get_by_experiment_season(
            experiment_name=experiment_name, season_name=season_name
        )
        season = season.set_info(season_info=info)
        return season

    # Delete Season by Experiment and Season Name
    @delete(path="/experiment/{experiment_name:str}/{season_name:str}")
    async def delete_season(self, experiment_name: str, season_name: str) -> None:
        season = Season.get_by_experiment_season(
            experiment_name=experiment_name, season_name=season_name
        )
        season.delete()

    # Get Experiment of the season by name
    @get(path="/{season_name:str}/experiment")
    async def get_season_experiment(self, season_name: str) -> Experiment:
        season = Season.get_by_name(season_name=season_name)
        experiment = season.get_experiment()
        return experiment

    # Get Season Plots
    @get(path="/{season_name:str}/plots")
    async def get_season_plots(self, season_name: str) -> List[Plot]:
        season = Season.get_by_name(season_name=season_name)
        if not season:
            return []
        plots = season.get_plots()
        return plots
