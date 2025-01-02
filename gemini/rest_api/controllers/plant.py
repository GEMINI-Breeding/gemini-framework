from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.plant import Plant
from gemini.rest_api.models import PlantInput, PlantOutput, PlantUpdate, RESTAPIBase, JSONB, str_to_dict

from typing import List, Annotated, Optional


class PlantController(Controller):

    # Get Plants
    @get()
    async def get_plants(
        self,
        plant_number: Optional[int] = None,
        plant_info: Optional[JSONB] = None,
        cultivar_accession: Optional[str] = None,
        cultivar_population: Optional[str] = None,
        plot_number: Optional[int] = None,
        plot_row_number: Optional[int] = None,
        plot_column_number: Optional[int] = None,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None,
    ) -> List[PlantOutput]:
        try:
            if plant_info is not None:
                plant_info = str_to_dict(plant_info)

            plants = Plant.search(
                plant_number=plant_number,
                plant_info=plant_info,
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
            )

            if plants is None:
                error_html = RESTAPIBase(
                    error="No plants found",
                    error_description="No plants were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            
            return plants
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while retrieving plants"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Plant by ID
    @get(path="/id/{plant_id:str}")
    async def get_plant_by_id(
        self, plant_id: str
    ) -> PlantOutput:
        try:
            plant = Plant.get_by_id(id=plant_id)
            if plant is None:
                error_html = RESTAPIBase(
                    error="Plant not found",
                    error_description="The plant with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return plant
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while retrieving the plant"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)


    # Create a new Plant
    @post()
    async def create(
        cls,
        data: Annotated[PlantInput, Body],
    ) -> PlantOutput:
        try:
            plant = Plant.create(
                plot_id=data.plot_id,
                plant_number=data.plant_number,
                plant_info=data.plant_info,
                cultivar_accession=data.cultivar_accession,
                cultivar_population=data.cultivar_population,
            )
            if plant is None:
                error_html = RESTAPIBase(
                    error="Plant not created",
                    error_description="The plant was not created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return plant
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while creating the plant"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Update Plant
    @patch(path="/id/{plant_id:str}")
    async def update(
        cls,
        plant_id: str,
        data: Annotated[PlantUpdate, Body],
    ) -> PlantOutput:
        try:
            plant = Plant.get_by_id(id=plant_id)
            if plant is None:
                error_html = RESTAPIBase(
                    error="Plant not found",
                    error_description="The plant with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            parameters = data.model_dump()
            plant = plant.update(**parameters)
            return plant
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while updating the plant"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Delete Plant
    @delete(path="/id/{plant_id:str}")
    async def delete(
        cls,
        plant_id: str,
    ) -> None:
        try:
            plant = Plant.get_by_id(id=plant_id)
            if plant is None:
                error_html = RESTAPIBase(
                    error="Plant not found",
                    error_description="The plant with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            plant.delete()
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while deleting the plant"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
