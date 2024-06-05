from litestar.controller import Controller
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar import Response

from pydantic import BaseModel, UUID4
from datetime import datetime, date

from gemini.api.experiment import Experiment
from gemini.api.cultivar import Cultivar

from typing import List, Annotated, Optional

class CultivarInput(BaseModel):
    cultivar_accession: str = "Test Accession"
    cultivar_population: str = "Test Population"
    experiment_name: str = "Test Experiment"
    cultivar_info: Optional[dict] = {}
    
    
class CultivarController(Controller):
    
    # Get Cultivars
    @get()
    async def get_cultivars(
        self,
        experiment_name: Optional[str] = "Test Experiment",
        cultivar_population: Optional[str] = "Test Population",
        cultivar_accession: Optional[str] = "Test Accession",
        cultivar_info: Optional[dict] = None
    ) -> List[Cultivar]:
        experiment = Experiment.get(experiment_name=experiment_name)
        cultivars = Cultivar.search(
            experiment_id=experiment.id,
            cultivar_population=cultivar_population,
            cultivar_accession=cultivar_accession,
            cultivar_info=cultivar_info
        )
        if cultivars is None:
            return Response(content="No cultivars found", status_code=404)
        return cultivars
    
    
    # Create a new Cultivar
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
        if cultivar is None:
            return Response(content="Cultivar already exists", status_code=409)
        return cultivar
    
    
    # Get Population Accessions
    @get('/{cultivar_population:str}/accessions')
    async def get_population_accessions(
        self,
        cultivar_population: str
    ) -> List[Cultivar]:
        cultivars = Cultivar.get_population_accessions(cultivar_population=cultivar_population)
        if cultivars is None:
            return Response(content="No cultivars found", status_code=404)
        return cultivars
    
    # Get by population and accession
    @get('/population/{cultivar_population:str}/accession/{cultivar_accession:str}')
    async def get_cultivar(
        self,
        cultivar_population: str,
        cultivar_accession: str
    ) -> Cultivar:
        cultivar = Cultivar.get(cultivar_population=cultivar_population, cultivar_accession=cultivar_accession)
        if cultivar is None:
            return Response(content="Cultivar not found", status_code=404)
        return cultivar
    
    # Get Cultivar Info
    @get('/population/{cultivar_population:str}/accession/{cultivar_accession:str}/info')
    async def get_cultivar_info(
        self,
        cultivar_population: str,
        cultivar_accession: str
    ) -> dict:
        cultivar = Cultivar.get(cultivar_population=cultivar_population, cultivar_accession=cultivar_accession)
        if cultivar is None:
            return Response(content="Cultivar not found", status_code=404)
        return cultivar.get_info()
    
    # Set Cultivar Info
    @patch('/population/{cultivar_population:str}/accession/{cultivar_accession:str}/info')
    async def set_cultivar_info(
        self,
        cultivar_population: str,
        cultivar_accession: str,
        data: dict
    ) -> dict:
        cultivar = Cultivar.get(cultivar_population=cultivar_population, cultivar_accession=cultivar_accession)
        if cultivar is None:
            return Response(content="Cultivar not found", status_code=404)
        cultivar.set_info(cultivar_info=data)
        return cultivar.get_info()