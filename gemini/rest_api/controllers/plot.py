from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller
from litestar.plugins.pydantic import PydanticDTO
from litestar.dto import DTOConfig

from gemini.api.plot import Plot
from gemini.rest_api.models import PlotInput, PlotOutput, PlotUpdate, RESTAPIError, JSONB, str_to_dict
from gemini.rest_api.models import (
    CultivarInput,
    CultivarOutput,
    ExperimentInput,
    SeasonInput,
    SiteInput,
    PlantInput,
    PlantOutput
)

from typing import List, Annotated, Optional

ExperimentInputDTO = PydanticDTO[Annotated[ExperimentInput, DTOConfig(
    exclude={"experiment_info", "experiment_start_date", "experiment_end_date"}
)]]

SeasonInputDTO = PydanticDTO[Annotated[SeasonInput, DTOConfig(
    exclude={"season_info", "season_start_date", "season_end_date"}
)]]

SiteInputDTO = PydanticDTO[Annotated[SiteInput, DTOConfig(
    exclude={"site_info", "site_city", "site_state", "site_country", "experiment_name"}
)]]


class PlotController(Controller):

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
                error_html = RESTAPIError(
                    error="No plots found",
                    error_description="No plots were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return plots
        except Exception as e:
            error_message = RESTAPIError(
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
                error_html = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return plot
        except Exception as e:
            error_message = RESTAPIError(
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
                cultivar_accession=data.cultivar_accession,
                cultivar_population=data.cultivar_population,
            )
            if plot is None:
                error_html = RESTAPIError(
                    error="Plot not created",
                    error_description="The plot was not created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return plot
        except Exception as e:
            error_message = RESTAPIError(
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
                error_html = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            plot = plot.update(
                plot_number=data.plot_number,
                plot_row_number=data.plot_row_number,
                plot_column_number=data.plot_column_number,
                plot_info=data.plot_info,
                plot_geometry_info=data.plot_geometry_info,
            )
            if plot is None:
                error_html = RESTAPIError(
                    error="Plot not updated",
                    error_description="The plot was not updated"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return plot
        except Exception as e:
            error_message = RESTAPIError(
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
                error_html = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = plot.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Failed to delete plot",
                    error_description="The plot was not deleted"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return None
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the plot"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Plot Plants
    @get(path="/id/{plot_id:str}/plants")
    async def get_plot_plants(
        self, plot_id: str
    ) -> List[PlantOutput]:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error_html = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            plants = plot.get_plants()
            if plants is None:
                error_html = RESTAPIError(
                    error="No plants found",
                    error_description="No plants were found for the given plot"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return plants
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the plants for the plot"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Plot Cultivars
    @get(path="/id/{plot_id:str}/cultivars")
    async def get_plot_cultivars(
        self, plot_id: str
    ) -> List[CultivarOutput]:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error_html = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            cultivars = plot.get_cultivars()
            if cultivars is None:
                error_html = RESTAPIError(
                    error="No cultivars found",
                    error_description="No cultivars were found for the given plot"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return cultivars
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the cultivars for the plot"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)

    # Add Plant to Plot
    @post(path="/id/{plot_id:str}/plants")
    async def add_plant_to_plot(
        self,
        plot_id: str,
        data: Annotated[PlantInput, Body]
    ) -> PlotOutput:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error_html = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            plot = plot.add_plant(
                plant_number=data.plant_number,
                cultivar_accession=data.cultivar_accession,
                cultivar_population=data.cultivar_population,
                plant_info=data.plant_info
            )
            if plot is None:
                error_html = RESTAPIError(
                    error="Plant not added",
                    error_description="The plant was not added to the plot"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return plot
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while adding the plant to the plot"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
    
    
    # Add Cultivar to Plot
    @post(path="/id/{plot_id:str}/cultivars")
    async def add_cultivar_to_plot(
        self,
        plot_id: str,
        data: Annotated[CultivarInput, Body]
    ) -> PlotOutput:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error_html = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            plot = plot.add_cultivar(
                cultivar_accession=data.cultivar_accession,
                cultivar_population=data.cultivar_population,
                cultivar_info=data.cultivar_info
            )
            if plot is None:
                error_html = RESTAPIError(
                    error="Cultivar not added",
                    error_description="The cultivar was not added to the plot"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return plot
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while adding the cultivar to the plot"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    

    # Update Plot Experiment
    @patch(path="/id/{plot_id:str}/experiment", dto=ExperimentInputDTO)
    async def update_plot_experiment(
        self,
        plot_id: str,
        data: Annotated[ExperimentInput, Body]
    ) -> PlotOutput:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error_html = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            plot = plot.set_experiment(
                experiment_name=data.experiment_name,
            )
            if plot is None:
                error_html = RESTAPIError(
                    error="Plot not updated",
                    error_description="The plot was not updated"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return plot
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the plot experiment"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Update Plot Season
    @patch(path="/id/{plot_id:str}/season", dto=SeasonInputDTO)
    async def update_plot_season(
        self,
        plot_id: str,
        data: Annotated[SeasonInput, Body]
    ) -> PlotOutput:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error_html = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            plot = plot.set_season(
                experiment_name=data.experiment_name,
                season_name=data.season_name,
            )
            if plot is None:
                error_html = RESTAPIError(
                    error="Plot not updated",
                    error_description="The plot was not updated"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return plot
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the plot season"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Update Plot Site
    @patch(path="/id/{plot_id:str}/site", dto=SiteInputDTO)
    async def update_plot_site(
        self,
        plot_id: str,
        data: Annotated[SiteInput, Body]
    ) -> PlotOutput:
        try:
            plot = Plot.get_by_id(id=plot_id)
            if plot is None:
                error_html = RESTAPIError(
                    error="Plot not found",
                    error_description="The plot with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            plot = plot.set_site(
                site_name=data.site_name,
            )
            if plot is None:
                error_html = RESTAPIError(
                    error="Plot not updated",
                    error_description="The plot was not updated"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return plot
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the plot site"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        


