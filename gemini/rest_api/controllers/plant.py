from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.plant import Plant
from gemini.rest_api.models import PlantInput, PlantOutput, PlantUpdate, RESTAPIError, JSONB, str_to_dict
from gemini.rest_api.models import CultivarInput, CultivarOutput 
from typing import List, Annotated, Optional

class PlantController(Controller):

    # Get all Plants
    @get()
    async def get_plants(
        self,
        plot_id: Optional[str] = None,
        plant_number: Optional[int] = None,
        cultivar_accession: Optional[str] = None,
        cultivar_population: Optional[str] = None,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None,
        plant_info: Optional[JSONB] = None
    ) -> List[PlantOutput]:
        try:
            if plant_info is not None:
                plant_info = str_to_dict(plant_info)

            plants = Plant.search(
                plot_id=plot_id,
                plant_number=plant_number,
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                plant_info=plant_info
            )

            if plants is None:
                error_html = RESTAPIError(
                    error="No plants found",
                    error_description="No plants were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return plants
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving plants"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Plant by ID
    @get(path="/id/{plant_id:int}")
    async def get_plant_by_id(
            self, plant_id: int
    ) -> PlantOutput:
        try:
            plant = Plant.get_by_id(id=plant_id)
            if plant is None:
                error_html = RESTAPIError(
                    error="Plant not found",
                    error_description="The plant with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return plant
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the plant"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Create a new Plant
    @post()
    async def create_plant(
        self,
        data: Annotated[PlantInput, Body]
    ) -> PlantOutput:
        try:
            if data.plant_info is not None:
                data.plant_info = str_to_dict(data.plant_info)

            plant = Plant.create(
                plot_id=data.plot_id,
                plant_number=data.plant_number,
                plant_info=data.plant_info,
                cultivar_accession=data.cultivar_accession,
                cultivar_population=data.cultivar_population
            )
            if plant is None:
                error_html = RESTAPIError(
                    error="Plant not created",
                    error_description="The plant could not be created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return plant
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the plant"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Update a Plant
    @patch(path="/id/{plant_id:int}")
    async def update_plant(
        self,
        plant_id: int,
        data: Annotated[PlantUpdate, Body]
    ) -> PlantOutput:
        try:
            plant = Plant.get_by_id(id=plant_id)
            if plant is None:
                error_html = RESTAPIError(
                    error="Plant not found",
                    error_description="The plant with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            plant = plant.update(
                plant_number=data.plant_number,
                plant_info=data.plant_info,
            )
            if plant is None:
                error_html = RESTAPIError(
                    error="Plant not updated",
                    error_description="The plant could not be updated"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return plant
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the plant"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Delete a Plant
    @delete(path="/id/{plant_id:int}")
    async def delete_plant(
        self,
        plant_id: int
    ) -> None:
        try:
            plant = Plant.get_by_id(id=plant_id)
            if plant is None:
                error_html = RESTAPIError(
                    error="Plant not found",
                    error_description="The plant with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = plant.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Failed to delete plant",
                    error_description="The plant could not be deleted"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return None
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the plant"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Plant Cultivar
    @get(path="/id/{plant_id:int}/cultivar")
    async def get_plant_cultivar(
        self,
        plant_id: int
    ) -> CultivarOutput:
        try:
            plant = Plant.get_by_id(id=plant_id)
            if plant is None:
                error_html = RESTAPIError(
                    error="Plant not found",
                    error_description="The plant with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            cultivar = plant.get_cultivar()
            if cultivar is None:
                error_html = RESTAPIError(
                    error="Cultivar not found",
                    error_description="The cultivar for the given plant was not found"
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
        
    # Set Plant Cultivar
    @post(path="/id/{plant_id:int}/cultivar")
    async def set_plant_cultivar(
        self,
        plant_id: int,
        cultivar: Annotated[CultivarInput, Body]
    ) -> PlantOutput:
        try:
            plant = Plant.get_by_id(id=plant_id)
            if plant is None:
                error_html = RESTAPIError(
                    error="Plant not found",
                    error_description="The plant with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            plant = plant.set_cultivar(
                cultivar_accession=cultivar.cultivar_accession,
                cultivar_population=cultivar.cultivar_population
            )
            if plant is None:
                error_html = RESTAPIError(
                    error="Cultivar not set",
                    error_description="The cultivar could not be set"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return plant
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while setting the cultivar"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
    



