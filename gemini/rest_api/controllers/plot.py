from litestar.controller import Controller
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.response import Stream
from litestar.serialization import encode_json
from litestar import Response

from pydantic import BaseModel, UUID4
from datetime import datetime, date
from collections.abc import AsyncGenerator

from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site
from gemini.api.cultivar import Cultivar
from gemini.api.plot import Plot, PlotSearchParameters
from gemini.api.plant import Plant

from typing import List, Annotated, Optional

async def plot_search_generator(search_parameters: PlotSearchParameters) -> AsyncGenerator[bytes, None]:
    plots = Plot.search(search_parameters=search_parameters)
    for plot in plots:
        plot = plot.model_dump_json(exclude_none=True)
        yield plot

class PlotInput(BaseModel):
    experiment_name: str = "Test Experiment"
    season_name: str = "2023"
    site_name: str = "Test Site"
    plot_number: int = 1
    plot_row_number: int = 1
    plot_column_number: int = 1
    plot_geometry_info: Optional[dict] = {}
    plot_info: Optional[dict] = {}
    cultivar_accession : Optional[str] = "Test Cultivar"
    cultivar_population : Optional[str] = "Test Population"
    
class PlotController(Controller):
    
    # Get Plots
    @get()
    async def get_plots(
        self,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None,
        plot_number: Optional[int] = None,
        plot_row_number: Optional[int] = None,
        plot_column_number: Optional[int] = None,
        plot_geometry_info: Optional[dict] = None,
        plot_info: Optional[dict] = None
    ) -> Stream:
        plot_search_parameters = PlotSearchParameters(
            experiment_name=experiment_name,
            season_name=season_name,
            site_name=site_name,
            plot_number=plot_number,
            plot_row_number=plot_row_number,
            plot_column_number=plot_column_number,
            plot_geometry_info=plot_geometry_info,
            plot_info=plot_info
        )
        return Stream(plot_search_generator(plot_search_parameters))
    
    # # Create a plot
    @post()
    async def create_plot(self, plot_input: PlotInput) -> Plot:
        plot = Plot.create(
            experiment_name=plot_input.experiment_name,
            season_name=plot_input.season_name,
            site_name=plot_input.site_name,
            plot_number=plot_input.plot_number,
            plot_row_number=plot_input.plot_row_number,
            plot_column_number=plot_input.plot_column_number,
            plot_geometry_info=plot_input.plot_geometry_info,
            plot_info=plot_input.plot_info,
            cultivar_accession=plot_input.cultivar_accession,
            cultivar_population=plot_input.cultivar_population
        )
        if not plot:
            return Response(status_code=400)
        return plot
    
    # Get Plot Info
    @get('/{plot_id:str}/info')
    async def get_plot_info(self, plot_id: str) -> dict:
        plot = Plot.get_by_id(plot_id)
        if not plot:
            return Response(status_code=404)
        return plot.get_info()
    
    # Set Plot Info
    @patch('/{plot_id:str}/info')
    async def set_plot_info(self, plot_id: str, data: dict) -> dict:
        plot = Plot.get_by_id(plot_id)
        if not plot:
            return Response(status_code=404)
        plot.set_info(data)
        return plot.get_info()
    
    # Delete Plot
    @delete('/{plot_id:str}')
    async def delete_plot(self, plot_id: str) -> None:
        plot = Plot.get_by_id(plot_id)
        if not plot:
            return Response(status_code=404)
        plot.delete()
        
    # Get Plot Experiment
    @get('/{plot_id:str}/experiment')
    async def get_plot_experiment(self, plot_id: str) -> Experiment:
        plot = Plot.get_by_id(plot_id)
        if not plot:
            return Response(status_code=404)
        return plot.experiment
    
    # Get Plot Season
    @get('/{plot_id:str}/season')
    async def get_plot_season(self, plot_id: str) -> Season:
        plot = Plot.get_by_id(plot_id)
        if not plot:
            return Response(status_code=404)
        return plot.season
    
    # Get Plot Site
    @get('/{plot_id:str}/site')
    async def get_plot_site(self, plot_id: str) -> Site:
        plot = Plot.get_by_id(plot_id)
        if not plot:
            return Response(status_code=404)
        return plot.site
    
    # Get Plot Cultivars
    @get('/{plot_id:str}/cultivars')
    async def get_plot_cultivars(self, plot_id: str) -> List[Cultivar]:
        plot = Plot.get_by_id(plot_id)
        if not plot:
            return Response(status_code=404)
        return plot.cultivars
        
   