from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.plot import Plot
from gemini.rest_api.models import PlotInput, PlotOutput, PlotUpdate, RESTAPIBase, JSONB, str_to_dict
from gemini.rest_api.models import (
    ExperimentOutput,
    SiteOutput,
    SeasonOutput,
    CultivarOutput
)


from typing import List, Annotated, Optional

class PlotController(Controller):

    # Get Plots
    @get()
    async def get_plots(
        self,
        plot_number: Optional[int] = None,
        plot_row_number: Optional[int] = None,
        plot_column_number: Optional[int] = None,
        plot_info: Optional[JSONB] = None,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None,
    ) -> List[PlotOutput]:
        try:
            if plot_info is not None:
                plot_info = str_to_dict(plot_info)

            plots = Plot.search(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                plot_info=plot_info,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
            )

            if plots is None:
                error_html = RESTAPIBase(
                    error="No plots found",
                    error_description="No plots were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            
            return plots
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while retrieving plots"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Plot by ID
    @get(path="/id/{plot_id:str}")
    async def get_plot_by_id(
        self, plot_id: str
    ) -> PlotOutput:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error_html = RESTAPIBase(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return plot
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while retrieving plot"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

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
            )
            if plot is None:
                error_html = RESTAPIBase(
                    error="Plot not created",
                    error_description="The plot was not created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return plot
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while creating the plot"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

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
                error_html = RESTAPIBase(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            parameters = data.model_dump()
            plot = plot.update(**parameters)
            return plot
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while updating the plot"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Delete Plot
    @delete(path="/id/{plot_id:str}")
    async def delete_plot(
        self, plot_id: str
    ) -> None:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error_html = RESTAPIBase(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            plot.delete()
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while deleting the plot"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Experiment for Plot
    @get(path="/id/{plot_id:str}/experiment")
    async def get_experiment_for_plot(
        self, plot_id: str
    ) -> ExperimentOutput:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error_html = RESTAPIBase(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            experiment = plot.experiment
            return experiment
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while retrieving the experiment for the plot"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Site for Plot
    @get(path="/id/{plot_id:str}/site")
    async def get_site_for_plot(
        self, plot_id: str
    ) -> SiteOutput:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error_html = RESTAPIBase(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            site = plot.site
            return site
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while retrieving the site for the plot"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Season for Plot
    @get(path="/id/{plot_id:str}/season")
    async def get_season_for_plot(
        self, plot_id: str
    ) -> SeasonOutput:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error_html = RESTAPIBase(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            season = plot.season
            return season
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while retrieving the season for the plot"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Cultivars for Plot
    @get(path="/id/{plot_id:str}/cultivars")
    async def get_cultivars_for_plot(
        self, plot_id: str
    ) -> List[CultivarOutput]:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error_html = RESTAPIBase(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            cultivars = plot.cultivars
            return cultivars
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while retrieving the cultivars for the plot"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

