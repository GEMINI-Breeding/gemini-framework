from litestar.contrib.pydantic import PydanticDTO
from litestar.controller import Controller
from litestar.dto import DTOConfig, DTOData
from litestar.enums import RequestEncodingType, MediaType
from litestar.params import Body
from litestar.handlers import get, post, patch, delete
from pydantic import BaseModel, UUID4

from typing import List, Annotated, Optional
from datetime import datetime, date
from uuid import UUID

from gemini.api.cultivar import Cultivar
from gemini.api.experiment import Experiment
from gemini.api.plot import Plot

class CultivarInput(BaseModel):
    cultivar_population: str
    cultivar_accession: Optional[str] = None
    cultivar_info: Optional[dict] = {}
    experiment_name: Optional[str] = None

class CultivarController(Controller):

    # Filter cultivars
    @get()
    async def get_cultivars(
        self, 
        cultivar_population: Optional[str] = None,
        cultivar_accession: Optional[str] = None,
        cultivar_info: Optional[dict] = None
        ) -> List[Cultivar]:
        cultivars = Cultivar.search(
            cultivar_population=cultivar_population,
            cultivar_accession=cultivar_accession,
            cultivar_info=cultivar_info
        )
        return cultivars
    
    # Get Cultivar by population
    @get(path="/{cultivar_population:str}")
    async def get_population_accessions(self, cultivar_population: str) -> List[Cultivar]:
        cultivars = Cultivar.get_accessions(cultivar_population=cultivar_population)
        return cultivars
    
    # Get Cultivar by population and accession
    @get(path="/{cultivar_population:str}/{cultivar_accession:str}")
    async def get_cultivar(self, cultivar_population: str, cultivar_accession: str) -> Cultivar:
        cultivar = Cultivar.get_by_name(
            cultivar_accession=cultivar_accession,
            cultivar_population=cultivar_population
        )
        return cultivar
    
    # Get Cultivar By ID
    @get(path="/id/{cultivar_id:uuid}")
    async def get_cultivar_by_id(self, cultivar_id: UUID) -> Cultivar:
        cultivar = Cultivar.get_by_id(cultivar_id)
        return cultivar
    
    # Create a new cultivar
    @post()
    async def create_cultivar(
        self, data: Annotated[CultivarInput, Body]
        ) -> Cultivar:
        cultivar = Cultivar.create(
            cultivar_population=data.cultivar_population,
            cultivar_accession=data.cultivar_accession,
            cultivar_info=data.cultivar_info,
            experiment_name=data.experiment_name
        )
        return cultivar
    
    # Get Cultivar info
    @get(path="/{cultivar_population:str}/{cultivar_accession:str}/info")
    async def get_cultivar_info(self, cultivar_population: str, cultivar_accession: str) -> dict:
        cultivar = Cultivar.get_by_name(
            cultivar_population=cultivar_population,
            cultivar_accession=cultivar_accession
        )
        return cultivar.cultivar_info
    
    # Set Cultivar info
    @patch(path="/{cultivar_population:str}/{cultivar_accession:str}/info")
    async def set_cultivar_info(
        self, cultivar_population: str, cultivar_accession: str, data: dict
        ) -> Cultivar:
        cultivar = Cultivar.get_by_name(
            cultivar_population=cultivar_population,
            cultivar_accession=cultivar_accession
        )
        cultivar = cultivar.set_info(cultivar_info=data)
        return cultivar
    
    # Delete Cultivar by population and accession
    @delete(path="/{cultivar_population:str}/{cultivar_accession:str}")
    async def delete_cultivar(
        self, cultivar_population: str, cultivar_accession: str
        ) -> None:
        cultivar = Cultivar.get_by_name(
            cultivar_population=cultivar_population,
            cultivar_accession=cultivar_accession
        )
        cultivar.delete()

    # Get Cultivar Experiments
    @get(path="/{cultivar_population:str}/{cultivar_accession:str}/experiments")
    async def get_cultivar_experiments(self, cultivar_population: str, cultivar_accession: str) -> List[Experiment]:
        cultivar = Cultivar.get_by_name(
            cultivar_population=cultivar_population,
            cultivar_accession=cultivar_accession
        )
        return cultivar.experiments
    
    # Get Cultivar Plots
    @get(path="/{cultivar_population:str}/{cultivar_accession:str}/plots")
    async def get_cultivar_plots(self, cultivar_population: str, cultivar_accession: str) -> List[Plot]:
        cultivar = Cultivar.get_by_name(
            cultivar_population=cultivar_population,
            cultivar_accession=cultivar_accession
        )
        if not cultivar:
            return []
        return cultivar.plots
    
