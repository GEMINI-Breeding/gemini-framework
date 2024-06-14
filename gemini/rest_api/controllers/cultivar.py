from litestar.controller import Controller
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar import Response

from pydantic import BaseModel, UUID4
from datetime import datetime, date

from gemini.api.experiment import Experiment
from gemini.api.cultivar import Cultivar

from gemini.rest_api.src.models import (
    CultivarBase,
    CultivarInput,
    CultivarOutput,
    CultivarSearch,
)

from typing import List, Annotated, Optional

class CultivarController(Controller):
    
    # Get Cultivars
    @get()
    async def get_cultivars(
        self,
        cultivar_population: Optional[str] = 'Default',
        cultivar_accession: Optional[str] = None,
        cultivar_info: Optional[dict] = None,
        experiment_name: Optional[str] = 'Default'
    ) -> List[Cultivar]:
        try:
            cultivars = Cultivar.search(
                cultivar_population=cultivar_population,
                cultivar_accession=cultivar_accession,
                cultivar_info=cultivar_info,
                experiment_name=experiment_name
            )
            if cultivars is None:
                return Response(content="No cultivars found", status_code=404)
            cultivars = [cultivar.model_dump() for cultivar in cultivars]
            cultivars = [CultivarOutput.model_validate(cultivar) for cultivar in cultivars]
            return cultivars
        except Exception as e:
            return Response(content=str(e), status_code=500)
            
    # Create a new Cultivar
    @post()
    async def create_cultivar(
        self, data: Annotated[CultivarInput, Body]
    ) -> Cultivar:
        try:
            cultivar = Cultivar.create(
                cultivar_population=data.cultivar_population,
                cultivar_accession=data.cultivar_accession,
                cultivar_info=data.cultivar_info,
                experiment_name=data.experiment_name
            )
            if cultivar is None:
                return Response(content="Cultivar already exists", status_code=409)
            cultivar = CultivarOutput.model_validate(cultivar.model_dump())
            return cultivar
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Delete Cultivar by Accession and Population
    @delete(path="/{cultivar_population:str}/{cultivar_accession:str}")
    async def delete_cultivar(
        self,
        cultivar_population: str,
        cultivar_accession: str
    ) -> None:
        try:
            cultivar = Cultivar.get(cultivar_population=cultivar_population, cultivar_accession=cultivar_accession)
            if cultivar is None:
                return Response(content="Cultivar not found", status_code=404)
            cultivar.delete()
            return Response(content="Cultivar deleted", status_code=200)
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Accessions for a given population
    @get(path="/{cultivar_population:str}/accessions")
    async def get_population_accessions(
        self, cultivar_population: str
    ) -> List[Cultivar]:
        try:
            cultivars = Cultivar.get_population_accessions(cultivar_population=cultivar_population)
            if cultivars is None:
                return Response(content="No accessions found", status_code=404)
            cultivars = [cultivar.model_dump() for cultivar in cultivars]
            cultivars = [CultivarOutput.model_validate(cultivar) for cultivar in cultivars]
            return cultivars
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Cultivar Info from accession and population
    @get(path="/{cultivar_population:str}/{cultivar_accession:str}/info")
    async def get_cultivar_info(
        self,
        cultivar_population: str,
        cultivar_accession: str
    ) -> dict:
        try:
            cultivar = Cultivar.get(cultivar_population=cultivar_population, cultivar_accession=cultivar_accession)
            if cultivar is None:
                return Response(content="Cultivar not found", status_code=404)
            return cultivar.get_info()
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Set Cultivar Info from accession and population
    @patch(path="/{cultivar_population:str}/{cultivar_accession:str}/info")
    async def set_cultivar_info(
        self,
        cultivar_population: str,
        cultivar_accession: str,
        data: dict
    ) -> dict:
        try:
            cultivar = Cultivar.get(cultivar_population=cultivar_population, cultivar_accession=cultivar_accession)
            if cultivar is None:
                return Response(content="Cultivar not found", status_code=404)
            cultivar.set_info(cultivar_info=data)
            return cultivar.get_info()
        except Exception as e:
            return Response(content=str(e), status_code=500)
    
    