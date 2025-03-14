from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.trait import Trait, GEMINITraitLevel
from gemini.rest_api.models import TraitInput, TraitOutput, TraitUpdate, JSONB, str_to_dict
from gemini.rest_api.models import TraitRecordInput, TraitRecordOutput, TraitRecordUpdate, TraitLevelSearch
from gemini.rest_api.models import RESTAPIError
from gemini.rest_api.models import DatasetOutput, DatasetInput
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
        experiment_name: Optional[str] = 'Experiment A'
    ) -> List[TraitOutput]:
        try:
            if trait_info is not None:
                trait_info = str_to_dict(trait_info)
            if trait_metrics is not None:
                trait_metrics = str_to_dict(trait_metrics)

            traits = Trait.search(
                trait_name=trait_name,
                trait_units=trait_units,
                trait_level=GEMINITraitLevel(trait_level_id) if trait_level_id else None,
                trait_info=trait_info,
                trait_metrics=trait_metrics,
                experiment_name=experiment_name
            )
            if traits is None:
                error_html = RESTAPIError(
                    error="No traits found",
                    error_description="No traits were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return traits
        except Exception as e:
            error_message = RESTAPIError(
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
                error_html = RESTAPIError(
                    error="Trait not found",
                    error_description="The trait with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return trait
        except Exception as e:
            error_message = RESTAPIError(
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
                trait_level=GEMINITraitLevel(data.trait_level_id),
                trait_info=data.trait_info,
                trait_metrics=data.trait_metrics,
                experiment_name=data.experiment_name,
            )
            if trait is None:
                error_html = RESTAPIError(
                    error="An error occurred while creating trait",
                    error_description="An error occurred while creating trait"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return trait
        except Exception as e:
            error_message = RESTAPIError(
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
                error_html = RESTAPIError(
                    error="Trait not found",
                    error_description="The trait with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            trait = trait.update(
                trait_name=data.trait_name,
                trait_units=data.trait_units,
                trait_level=GEMINITraitLevel(data.trait_level_id) if data.trait_level_id else None,
                trait_info=data.trait_info,
                trait_metrics=data.trait_metrics,
            )
            if trait is None:
                error_html = RESTAPIError(
                    error="An error occurred while updating trait",
                    error_description="An error occurred while updating trait"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return trait
        except Exception as e:
            error_message = RESTAPIError(
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
                error_html = RESTAPIError(
                    error="Trait not found",
                    error_description="The trait with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = trait.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Failed to delete trait",
                    error_description="The trait was not deleted"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return None
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting trait"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Trait Datasets
    @get(path="/id/{trait_id:str}/datasets")
    async def get_trait_datasets(
        self, trait_id: str
    ) -> List[DatasetOutput]:
        try:
            trait = Trait.get_by_id(id=trait_id)
            if trait is None:
                error_html = RESTAPIError(
                    error="Trait not found",
                    error_description="The trait with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            datasets = trait.get_datasets()
            if datasets is None:
                error_html = RESTAPIError(
                    error="No datasets found",
                    error_description="No datasets were found for the given trait"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return datasets
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving trait datasets"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Create Trait Dataset
    @post(path="/id/{trait_id:str}/datasets")
    async def create_trait_dataset(
        self,
        trait_id: str,
        data: Annotated[DatasetInput, Body]
    ) -> DatasetOutput:
        try:
            trait = Trait.get_by_id(id=trait_id)
            if trait is None:
                error_html = RESTAPIError(
                    error="Trait not found",
                    error_description="The trait with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            dataset = trait.create_dataset(
                dataset_name=data.dataset_name,
                dataset_info=data.dataset_info,
                collection_date=data.collection_date,
                experiment_name=data.experiment_name,
            )
            if dataset is None:
                error_html = RESTAPIError(
                    error="An error occurred while creating dataset",
                    error_description="An error occurred while creating dataset"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return dataset
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating dataset"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)