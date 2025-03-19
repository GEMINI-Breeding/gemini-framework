from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.season import Season
from gemini.rest_api.models import ( 
    SeasonInput, 
    SeasonOutput, 
    SeasonUpdate, 
    RESTAPIError, 
    JSONB, 
    str_to_dict
)

from typing import List, Annotated, Optional

class SeasonController(Controller):

    # Get All Seasons
    @get(path="/all")
    async def get_all_seasons(self) -> List[SeasonOutput]:
        try:
            seasons = Season.get_all()
            if seasons is None:
                error_html = RESTAPIError(
                    error="No seasons found",
                    error_description="No seasons were found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return seasons
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving all seasons"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)

    # Get Seasons
    @get()
    async def get_seasons(
        self,
        season_name: Optional[str] = None,
        season_info: Optional[JSONB] = None,
        season_start_date: Optional[str] = None,
        season_end_date: Optional[str] = None,
        experiment_name: Optional[str] = 'Experiment A'
    ) -> List[SeasonOutput]:
        try:
            if season_info is not None:
                season_info = str_to_dict(season_info)

            seasons = Season.search(
                season_name=season_name,
                season_info=season_info,
                season_start_date=season_start_date,
                season_end_date=season_end_date,
                experiment_name=experiment_name,
            )
            if seasons is None:
                error_html = RESTAPIError(
                    error="No seasons found",
                    error_description="No seasons were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return seasons
        except Exception as e:
            error_message = RESTAPIError(
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
                error_html = RESTAPIError(
                    error="Season not found",
                    error_description="The season with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return season
        except Exception as e:
            error_message = RESTAPIError(
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
                error_html = RESTAPIError(
                    error="Season not created",
                    error_description="The season could not be created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return season
        except Exception as e:
            error_message = RESTAPIError(
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
                error_html = RESTAPIError(
                    error="Season not found",
                    error_description="The season with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            season = season.update(
                season_name=data.season_name,
                season_info=data.season_info,
                season_start_date=data.season_start_date,
                season_end_date=data.season_end_date
            )
            if season is None:
                error_html = RESTAPIError(
                    error="Season not updated",
                    error_description="The season could not be updated"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return season
        except Exception as e:
            error_message = RESTAPIError(
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
                error_html = RESTAPIError(
                    error="Season not found",
                    error_description="The season with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = season.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Season not deleted",
                    error_description="The season could not be deleted"
                ).to_html()
                return Response(content=error_html, status_code=500)
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the season"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
    
