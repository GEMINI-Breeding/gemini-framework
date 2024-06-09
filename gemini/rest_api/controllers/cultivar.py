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
        cultivar_population: Optional[str] = None,
        cultivar_accession: Optional[str] = None,
        cultivar_info: Optional[dict] = None
    ) -> List[Cultivar]:
        try:
            cultivars = Cultivar.search(
                cultivar_population=cultivar_population,
                cultivar_accession=cultivar_accession,
                cultivar_info=cultivar_info
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
                cultivar_info=data.cultivar_info
            )
            if cultivar is None:
                return Response(content="Cultivar already exists", status_code=409)
            cultivar = CultivarOutput.model_validate(cultivar.model_dump())
            return cultivar
        except Exception as e:
            return Response(content=str(e), status_code=500)
    