from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.dataset_type import DatasetType
from gemini.rest_api.models import DatasetTypeInput, DatasetTypeOutput, RESTAPIError, str_to_dict, JSONB

from typing import List, Annotated, Optional

class DatasetTypeController(Controller):

    # Get Dataset Types
    @get()
    async def get_dataset_types(
        self,
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
        self, dataset_type_id: int
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
                error_description="An error occurred while retrieving dataset type"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Create a new Dataset Type
    @post()
    async def create_dataset_type(
        self, data: Annotated[DatasetTypeInput, Body]
    ) -> DatasetTypeOutput:
        try:
            dataset_type = DatasetType.create(
                dataset_type_name=data.dataset_type_name,
                dataset_type_info=data.dataset_type_info
            )
            if dataset_type is None:
                error_html = RESTAPIError(
                    error="Dataset type not created",
                    error_description="The dataset type could not be created"
                ).to_html()
                return Response(content=error_html, status_code=400)
            return dataset_type
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the dataset type"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)

    