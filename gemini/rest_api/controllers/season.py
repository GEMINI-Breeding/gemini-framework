from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.season import Season
from gemini.rest_api.models import SeasonInput, SeasonOutput, SeasonUpdate, RESTAPIBase, JSONB, str_to_dict

from typing import List, Annotated, Optional

class SeasonController(Controller):

    # Get Seasons
    @get()
    async def get_seasons(
        self,
        season_name: Optional[str] = None,
        season_info: Optional[JSONB] = None,
        experiment_name: Optional[str] = None,
    ) -> List[SeasonOutput]:
        try:
            if season_info is not None:
                season_info = str_to_dict(season_info)

            seasons = Season.search(
                season_name=season_name,
                season_info=season_info,
                experiment_name=experiment_name,
            )

            if seasons is None:
                error_html = RESTAPIBase(
                    error="No seasons found",
                    error_description="No seasons were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            
            return seasons
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while retrieving seasons"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Season by ID
    @get(path="/id/{season_id:str}")
    async def get_season_by_id(
        self, season_id: str
    ) -> SeasonOutput:
        try:
            season = Season.get_by_id(id=season_id)
            if season is None:
                error_html = RESTAPIBase(
                    error="Season not found",
                    error_description="The season with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return season
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while retrieving the season"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Create Season
    @post()
    async def create_season(
        self,
        data: Annotated[SeasonInput, Body]
    ) -> SeasonOutput:
        try:
            season = Season.create(
                season_name=data.season_name,
                season_info=data.season_info,
                season_start_date=data.season_start_date,
                season_end_date=data.season_end_date,
                experiment_name=data.experiment_name,
            )
            if season is None:
                error_html = RESTAPIBase(
                    error="Season not created",
                    error_description="The season could not be created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return season
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while creating the season"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Update Season
    @patch(path="/id/{season_id:str}")
    async def update_season(
        self,
        season_id: str,
        data: Annotated[SeasonUpdate, Body]
    ) -> SeasonOutput:
        try:
            season = Season.get_by_id(id=season_id)
            if season is None:
                error_html = RESTAPIBase(
                    error="Season not found",
                    error_description="The season with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            parameters = data.model_dump()
            season.update(**parameters)
            return season
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while updating the season"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Delete Season
    @delete(path="/id/{season_id:str}")
    async def delete_season(
        self, season_id: str
    ) -> None:
        try:
            season = Season.get_by_id(id=season_id)
            if season is None:
                error_html = RESTAPIBase(
                    error="Season not found",
                    error_description="The season with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            season.delete()
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while deleting the season"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)