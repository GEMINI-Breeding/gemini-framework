from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.dataset_type import DatasetType
from gemini.rest_api.models import (
    DatasetTypeInput, 
    DatasetTypeOutput,
    DatasetTypeUpdate, 
    RESTAPIError, 
    str_to_dict, 
    JSONB
)

from typing import List, Annotated, Optional

class DatasetTypeController(Controller):

    # Get Dataset Types
    @get()
    async def get_dataset_types(
        cls,
        dataset_type_name: Optional[str] = None,
        dataset_type_info: Optional[JSONB] = None
    ) -> List[DatasetTypeOutput]:
        try:
            if dataset_type_info is not None:
                dataset_type_info = str_to_dict(dataset_type_info)

            dataset_types = DatasetType.search(
                dataset_type_name=dataset_type_name,
                dataset_type_info=dataset_type_info
            )
            if dataset_types is None:
                error_html = RESTAPIError(
                    error="No dataset types found",
                    error_description="No dataset types were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return dataset_types
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving dataset types"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Dataset Type by ID
    @get(path="/id/{dataset_type_id:int}")
    async def get_dataset_type_by_id(
        cls, dataset_type_id: int
    ) -> DatasetTypeOutput:
        try:
            dataset_type = DatasetType.get_by_id(id=dataset_type_id)
            if dataset_type is None:
                error_html = RESTAPIError(
                    error="Dataset type not found",
                    error_description="The dataset type with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return dataset_type
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the dataset type"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Create Dataset Type
    @post()
    async def create_dataset_type(
        cls, dataset_type: Annotated[DatasetTypeInput, Body]
    ) -> DatasetTypeOutput:
        try:
            dataset_type = DatasetType.create(
                dataset_type_name=dataset_type.dataset_type_name,
                dataset_type_info=dataset_type.dataset_type_info
            )
            if dataset_type is None:
                error_html = RESTAPIError(
                    error="Dataset type not created",
                    error_description="The dataset type was not created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return dataset_type
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the dataset type"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Update Dataset Type
    @patch(path="/id/{dataset_type_id:int}")
    async def update_dataset_type(
        cls, dataset_type_id: int, dataset_type: Annotated[DatasetTypeUpdate, Body]
    ) -> DatasetTypeOutput:
        try:
            dataset_type = DatasetType.get_by_id(id=dataset_type_id)
            if dataset_type is None:
                error_html = RESTAPIError(
                    error="Dataset type not found",
                    error_description="The dataset type with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            dataset_type = DatasetType.update(
                dataset_type_name=dataset_type.dataset_type_name,
                dataset_type_info=dataset_type.dataset_type_info
            )
            if dataset_type is None:
                error_html = RESTAPIError(
                    error="Dataset type not updated",
                    error_description="The dataset type could not be updated"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return dataset_type
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the dataset type"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Delete Dataset Type
    @delete(path="/id/{dataset_type_id:int}")
    async def delete_dataset_type(
        cls, dataset_type_id: int
    ) -> None:
        try:
            dataset_type = DatasetType.get_by_id(id=dataset_type_id)
            if dataset_type is None:
                error_html = RESTAPIError(
                    error="Dataset type not found",
                    error_description="The dataset type with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = dataset_type.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Dataset type not deleted",
                    error_description="The dataset type could not be deleted"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return None
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the dataset type"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)


            
    



