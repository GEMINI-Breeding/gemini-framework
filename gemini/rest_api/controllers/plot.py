from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from pydantic import BaseModel

from gemini.api.plot import Plot
from gemini.rest_api.models import PlotInput, PlotOutput, PlotUpdate, RESTAPIError, JSONB, str_to_dict
from gemini.rest_api.models import (
    CultivarOutput,
    PlantOutput,
    ExperimentOutput,
    SeasonOutput,
    SiteOutput
)

from typing import List, Annotated, Optional

class PlotExperimentInput(BaseModel):
    experiment_name: str

class PlotSeasonInput(BaseModel):
    experiment_name: str
    season_name: str

class PlotSiteInput(BaseModel):
    site_name: str

class PlotCultivarInput(BaseModel):
    cultivar_accession: str
    cultivar_population: str
    cultivar_info: Optional[JSONB] = None

class PlotPlantInput(BaseModel):
    plant_number: int
    cultivar_accession: str
    cultivar_population: str
    plant_info: Optional[JSONB] = None


class PlotController(Controller):

    # Get All Plots
    @get(path="/all")
    async def get_all_plots(self) -> List[PlotOutput]:
        try:
            plots = Plot.get_all()
            if plots is None:
                error = RESTAPIError(
                    error="No plots found",
                    error_description="No plots were found"
                )
                return Response(content=error, status_code=404)
            return plots
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving all plots"
            )
            return Response(content=error, status_code=500)

    # Get Plots
    @get()
    async def get_plots(
        self,
        plot_number: Optional[int] = None,
        plot_row_number: Optional[int] = None,
        plot_column_number: Optional[int] = None,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None
    ) -> List[PlotOutput]:
        try:

            plots = Plot.search(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )

            if plots is None:
                error = RESTAPIError(
                    error="No plots found",
                    error_description="No plots were found with the given search criteria"
                )
                return Response(content=error, status_code=404)
            return plots
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving plots"
            )
            return Response(content=error, status_code=500)
        
    # Get Plot by ID
    @get(path="/id/{plot_id:str}")
    async def get_plot_by_id(
        self, plot_id: str
    ) -> PlotOutput:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                )
                return Response(content=error, status_code=404)
            return plot
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving plot"
            )
            return Response(content=error, status_code=500)

    # Create a new Plot
    @post()
    async def create_plot(
        self,
        data: Annotated[PlotInput, Body]
    ) -> PlotOutput:
        try:
            plot = Plot.create(
                plot_number=data.plot_number,
                plot_row_number=data.plot_row_number,
                plot_column_number=data.plot_column_number,
                plot_info=data.plot_info,
                experiment_name=data.experiment_name,
                season_name=data.season_name,
                site_name=data.site_name,
                cultivar_accession=data.cultivar_accession,
                cultivar_population=data.cultivar_population,
            )
            if plot is None:
                error = RESTAPIError(
                    error="Plot not created",
                    error_description="The plot was not created"
                )
                return Response(content=error, status_code=500)
            return plot
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the plot"
            )
            return Response(content=error, status_code=500)
        
    # Update Plot
    @patch(path="/id/{plot_id:str}")
    async def update_plot(
        self,
        plot_id: str,
        data: Annotated[PlotUpdate, Body]
    ) -> PlotOutput:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                )
                return Response(content=error, status_code=404)
            plot = plot.update(
                plot_number=data.plot_number,
                plot_row_number=data.plot_row_number,
                plot_column_number=data.plot_column_number,
                plot_info=data.plot_info,
                plot_geometry_info=data.plot_geometry_info,
            )
            if plot is None:
                error = RESTAPIError(
                    error="Plot not updated",
                    error_description="The plot was not updated"
                )
                return Response(content=error, status_code=500)
            return plot
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the plot"
            )
            return Response(content=error, status_code=500)
        
    # Delete Plot
    @delete(path="/id/{plot_id:str}")
    async def delete_plot(
        self, plot_id: str
    ) -> None:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                )
                return Response(content=error, status_code=404)
            is_deleted = plot.delete()
            if not is_deleted:
                error = RESTAPIError(
                    error="Failed to delete plot",
                    error_description="The plot was not deleted"
                )
                return Response(content=error, status_code=500)
            return None
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the plot"
            )
            return Response(content=error, status_code=500)
        
        
    # Get Plot Cultivars
    @get(path="/id/{plot_id:str}/cultivars")
    async def get_plot_cultivars(
        self, plot_id: str
    ) -> List[CultivarOutput]:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                )
                return Response(content=error, status_code=404)
            cultivars = plot.get_associated_cultivars()
            if cultivars is None:
                error_html = RESTAPIError(
                    error="No cultivars found",
                    error_description="No cultivars were found for the given plot"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return cultivars
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the cultivars for the plot"
            )
            return Response(content=error, status_code=500)
        
    # Get Plot Experiment
    @get(path="/id/{plot_id:str}/experiment")
    async def get_plot_experiment(
        self, plot_id: str
    ) -> ExperimentOutput:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                )
                return Response(content=error, status_code=404)
            experiment = plot.get_associated_experiment()
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="The experiment for the given plot was not found"
                )
                return Response(content=error, status_code=404)
            return experiment
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment for the plot"
            )
            return Response(content=error, status_code=500)
        
    # Get Plot Season
    @get(path="/id/{plot_id:str}/season")
    async def get_plot_season(
        self, plot_id: str
    ) -> SeasonOutput:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                )
                return Response(content=error, status_code=404)
            season = plot.get_associated_season()
            if season is None:
                error = RESTAPIError(
                    error="Season not found",
                    error_description="The season for the given plot was not found"
                )
                return Response(content=error, status_code=404)
            return season
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the season for the plot"
            )
            return Response(content=error, status_code=500)
        
    # Get Plot Site
    @get(path="/id/{plot_id:str}/site")
    async def get_plot_site(
        self, plot_id: str
    ) -> SiteOutput:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                )
                return Response(content=error, status_code=404)
            site = plot.get_associated_site()
            if site is None:
                error = RESTAPIError(
                    error="Site not found",
                    error_description="The site for the given plot was not found"
                )
                return Response(content=error, status_code=404)
            return site
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the site for the plot"
            )
            return Response(content=error, status_code=500)

