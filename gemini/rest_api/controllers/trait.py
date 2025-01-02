from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.trait import Trait
from gemini.rest_api.models import TraitInput, TraitOutput, TraitUpdate, RESTAPIBase, JSONB, str_to_dict

from typing import List, Annotated, Optional

class TraitController(Controller):

    # Get Traits
    @get()
    async def get_traits(
        self,
        trait_name: Optional[str] = None,
        trait_units: Optional[str] = None,
        trait_level_id: Optional[int] = None,
        trait_info: Optional[JSONB] = None,
        trait_metrics: Optional[JSONB] = None,
        experiment_name: Optional[str] = 'Default',
    ) -> List[TraitOutput]:
        try:
            if trait_info is not None:
                trait_info = str_to_dict(trait_info)
            if trait_metrics is not None:
                trait_metrics = str_to_dict(trait_metrics)

            traits = Trait.search(
                trait_name=trait_name,
                trait_units=trait_units,
                trait_level_id=trait_level_id,
                trait_info=trait_info,
                trait_metrics=trait_metrics,
                experiment_name=experiment_name,
            )

            if traits is None:
                error_html = RESTAPIBase(
                    error="No traits found",
                    error_description="No traits were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            
            return traits
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while retrieving traits"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Trait by ID
    @get(path="/id/{trait_id:str}")
    async def get_trait_by_id(
        self, trait_id: str
    ) -> TraitOutput:
        try:
            trait = Trait.get_by_id(id=trait_id)
            if trait is None:
                error_html = RESTAPIBase(
                    error="Trait not found",
                    error_description="The trait with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return trait
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while retrieving trait"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Create Trait
    @post()
    async def create_trait(
        self,
        data: Annotated[TraitInput, Body]
    ) -> TraitOutput:
        try:
            trait = Trait.create(
                trait_name=data.trait_name,
                trait_units=data.trait_units,
                trait_level_id=data.trait_level_id,
                trait_info=data.trait_info,
                trait_metrics=data.trait_metrics,
                experiment_name=data.experiment_name,
            )
            if trait is None:
                error_html = RESTAPIBase(
                    error="An error occurred while creating trait",
                    error_description="An error occurred while creating trait"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return trait
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while creating trait"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Update Trait
    @patch(path="/id/{trait_id:str}")
    async def update_trait(
        self,
        trait_id: str,
        data: Annotated[TraitUpdate, Body]
    ) -> TraitOutput:
        try:
            trait = Trait.get_by_id(id=trait_id)
            if trait is None:
                error_html = RESTAPIBase(
                    error="Trait not found",
                    error_description="The trait with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            parameters = data.model_dump()
            trait = trait.update(**parameters)
            return trait
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while updating trait"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Delete Trait
    @delete(path="/id/{trait_id:str}")
    async def delete_trait(
        self, trait_id: str
    ) -> None:
        try:
            trait = Trait.get_by_id(id=trait_id)
            if trait is None:
                error_html = RESTAPIBase(
                    error="Trait not found",
                    error_description="The trait with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            trait.delete()
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while deleting trait"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)