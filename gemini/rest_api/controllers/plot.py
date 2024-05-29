from litestar.contrib.pydantic import PydanticDTO
from litestar.controller import Controller
from litestar.response import Stream
from litestar import Request
from litestar.dto import DTOConfig, DTOData
from litestar.enums import RequestEncodingType, MediaType
from litestar.params import Body
from litestar.handlers import get, post, patch, delete
from litestar.serialization import encode_json, default_serializer
from pydantic import BaseModel
from collections.abc import AsyncGenerator
from typing import List, Annotated, Optional
from datetime import datetime, date
from uuid import UUID

from gemini.api.plot import Plot
from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site
from gemini.api.cultivar import Cultivar

async def plot_generator(**params) -> AsyncGenerator[bytes, None]:
    plots = Plot.search(**params)
    for plot in plots:
        plot = plot.model_dump_json()
        yield plot

class PlotInput(BaseModel):
    plot_number: int
    plot_row_number: int
    plot_column_number: int
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    cultivar_population: Optional[str] = None
    cultivar_accession: Optional[str] = None
    plot_info: Optional[dict] = {}
    plot_geometry_info: Optional[dict] = {}


class PlotController(Controller):

    # Filter plots
    @get()
    async def get_plots(
        self,
        plot_number: Optional[int] = None,
        plot_row_number: Optional[int] = None,
        plot_column_number: Optional[int] = None,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None,
        cultivar_population: Optional[str] = None,
        cultivar_accession: Optional[str] = None,
        plot_info: Optional[dict] = None,
        plot_geometry_info: Optional[dict] = None,
    ) -> Stream:
            return Stream(
                plot_generator(
                    plot_number=plot_number,
                    plot_row_number=plot_row_number,
                    plot_column_number=plot_column_number,
                    experiment_name=experiment_name,
                    season_name=season_name,
                    site_name=site_name,
                    cultivar_population=cultivar_population,
                    cultivar_accession=cultivar_accession,
                    plot_info=plot_info,
                    plot_geometry_info=plot_geometry_info
                )
            )
    
    # Get Plot by ID
    @get(path="/id/{plot_id:uuid}")
    async def get_plot_by_id(self, plot_id: UUID) -> Plot:
        plot = Plot.get_by_id(plot_id)
        return plot


    # Create a new plot
    @post()
    async def create_plot(
        self, data: Annotated[PlotInput, Body]
        ) -> Plot:
        plot = Plot.create(
            plot_number=data.plot_number,
            plot_row_number=data.plot_row_number,
            plot_column_number=data.plot_column_number,
            experiment_name=data.experiment_name,
            season_name=data.season_name,
            site_name=data.site_name,
            cultivar_population=data.cultivar_population,
            cultivar_accession=data.cultivar_accession,
            plot_info=data.plot_info,
            plot_geometry_info=data.plot_geometry_info
        )
        return plot
    
    # Delete Plot Based on ID
    @delete(path="/id/{plot_id:uuid}")
    async def delete_plot(self, plot_id: UUID) -> None:
        plot = Plot.get_by_id(plot_id)
        plot.delete()

    # Get Plot info based on ID
    @get(path="/id/{plot_id:uuid}/info")
    async def get_plot_info(self, plot_id: UUID) -> dict:
        plot = Plot.get_by_id(plot_id)
        plot_info = plot.get_info()
        return plot_info
    
    # Set Plot info based on ID
    @patch(path="/id/{plot_id:uuid}/info")
    async def set_plot_info(
        self, plot_id: UUID, data: dict
    ) -> Plot:
        plot = Plot.get_by_id(plot_id)
        plot = plot.set_info(plot_info=data)
        return plot
    
    # Get Plot geometry info based on ID
    @get(path="/id/{plot_id:uuid}/geometry")
    async def get_plot_geometry_info(self, plot_id: UUID) -> dict:
        plot = Plot.get_by_id(plot_id)
        plot_geometry_info = plot.get_geometry()
        return plot_geometry_info
    
    # Set Plot geometry info based on ID
    @patch(path="/id/{plot_id:uuid}/geometry")
    async def set_plot_geometry_info(
        self, plot_id: UUID, data: dict
    ) -> Plot:
        plot = Plot.get_by_id(plot_id)
        plot = plot.set_geometry(geometry_info=data)
        return plot
    
    # Get Experiment for a plot
    @get(path="/id/{plot_id:uuid}/experiment")
    async def get_plot_experiment(self, plot_id: UUID) -> Experiment:
        plot = Plot.get_by_id(plot_id)
        experiment = plot.get_experiment()
        return experiment
    
    # Get Season for a plot
    @get(path="/id/{plot_id:uuid}/season")
    async def get_plot_season(self, plot_id: UUID) -> Season:
        plot = Plot.get_by_id(plot_id)
        season = plot.get_season()
        return season
    
    # Get Site for a plot
    @get(path="/id/{plot_id:uuid}/site")
    async def get_plot_site(self, plot_id: UUID) -> Site:
        plot = Plot.get_by_id(plot_id)
        site = plot.get_site()
        return site
    
    # Get Cultivars for a plot
    @get(path="/id/{plot_id:uuid}/cultivars")
    async def get_plot_cultivars(self, plot_id: UUID) -> List[Cultivar]:
        plot = Plot.get_by_id(plot_id)
        cultivars = plot.get_cultivars()
        return cultivars
    

    

  
 
        

