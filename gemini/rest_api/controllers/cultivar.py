from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.cultivar import Cultivar
from gemini.rest_api.models import (
    CultivarInput,
    CultivarOutput,
    CultivarUpdate,
    RESTAPIError,
    str_to_dict,
    JSONB
)

from typing import List, Annotated, Optional

class CultivarController(Controller):

    # Get All Cultivars
    @get(path="/all")
    async def get_all_cultivars(self) -> List[CultivarOutput]:
        try:
            cultivars = Cultivar.get_all()
            if cultivars is None:
                error_html = RESTAPIError(
                    error="No cultivars found",
                    error_description="No cultivars were found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return cultivars
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving all cultivars"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)

    # Get Cultivars
    @get()
    async def get_cultivars(
        self,
        cultivar_population: Optional[str] = None,
        cultivar_accession: Optional[str] = None,
        cultivar_info: Optional[JSONB] = None,
        experiment_name: Optional[str] = 'Experiment A'
    ) -> List[CultivarOutput]:
        try:
            if cultivar_info is not None:
                cultivar_info = str_to_dict(cultivar_info)

            cultivars = Cultivar.search(
                cultivar_population=cultivar_population,
                cultivar_accession=cultivar_accession,
                cultivar_info=cultivar_info,
                experiment_name=experiment_name
            )
            if cultivars is None:
                error_html = RESTAPIError(
                    error="No cultivars found",
                    error_description="No cultivars were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return cultivars
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving cultivars"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Cultivar by ID
    @get(path="/id/{cultivar_id:str}")
    async def get_cultivar_by_id(
        self, cultivar_id: str
    ) -> CultivarOutput:
        try:
            cultivar = Cultivar.get_by_id(id=cultivar_id)
            if cultivar is None:
                error_html = RESTAPIError(
                    error="Cultivar not found",
                    error_description="The cultivar with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return cultivar
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the cultivar"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Create a new Cultivar
    @post()
    async def create_cultivar(
        self, data: Annotated[CultivarInput, Body]
    ) -> CultivarOutput:
        try:
            cultivar = Cultivar.create(
                cultivar_population=data.cultivar_population,
                cultivar_accession=data.cultivar_accession,
                cultivar_info=data.cultivar_info,
                experiment_name=data.experiment_name
            )
            if cultivar is None:
                error_html = RESTAPIError(
                    error="Cultivar creation failed",
                    error_description="The cultivar could not be created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return cultivar
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the cultivar"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Update Existing Cultivar
    @patch(path="/id/{cultivar_id:str}")
    async def update_cultivar(
        self, cultivar_id: str, data: Annotated[CultivarUpdate, Body]
    ) -> CultivarOutput:
        try:
            cultivar = Cultivar.get_by_id(id=cultivar_id)
            if cultivar is None:
                error_html = RESTAPIError(
                    error="Cultivar not found",
                    error_description="The cultivar with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            cultivar = cultivar.update(
                cultivar_accession=data.cultivar_accession,
                cultivar_population=data.cultivar_population,
                cultivar_info=data.cultivar_info
            )
            if cultivar is None:
                error_html = RESTAPIError(
                    error="Cultivar update failed",
                    error_description="The cultivar could not be updated"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return cultivar
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the cultivar"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Delete Cultivar
    @delete(path="/id/{cultivar_id:str}")
    async def delete_cultivar(
        self, cultivar_id: str
    ) -> None:
        try:
            cultivar = Cultivar.get_by_id(id=cultivar_id)
            if cultivar is None:
                error_html = RESTAPIError(
                    error="Cultivar not found",
                    error_description="The cultivar with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = cultivar.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Cultivar deletion failed",
                    error_description="The cultivar could not be deleted"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return None
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the cultivar"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Population Accessions
    @get(path="/accessions/{cultivar_population:str}")
    async def get_population_accessions(
        self, cultivar_population: str
    ) -> List[CultivarOutput]:
        try:
            cultivars = Cultivar.get_population_accessions(cultivar_population=cultivar_population)
            if cultivars is None:
                error_html = RESTAPIError(
                    error="No cultivars found",
                    error_description="No cultivars were found in the given population"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return cultivars
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving cultivars"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)

