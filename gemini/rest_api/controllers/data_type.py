from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.data_type import DataType
from gemini.rest_api.models import DataTypeInput, DataTypeOutput, RESTAPIError, JSONB, str_to_dict

from typing import List, Annotated, Optional

class DataTypeController(Controller):

    # Get Data Types
    @get()
    async def get_data_types(
        self,
        data_type_name: Optional[str] = None,
        data_type_info: Optional[JSONB] = None
    ) -> List[DataTypeOutput]:
        try:

            if data_type_info is not None:
                data_type_info = str_to_dict(data_type_info)

            data_types = DataType.search(
                data_type_name=data_type_name,
                data_type_info=data_type_info
            )
            if data_types is None:
                error_html = RESTAPIError(
                    error="No data types found",
                    error_description="No data types were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return data_types
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving data types"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Data Type by ID
    @get(path="/id/{data_type_id:int}")
    async def get_data_type_by_id(
        self, data_type_id: int
    ) -> DataTypeOutput:
        try:
            data_type = DataType.get_by_id(id=data_type_id)
            if data_type is None:
                error_html = RESTAPIError(
                    error="Data type not found",
                    error_description="The data type with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return data_type
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the data type"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Create a new Data Format
    @post()
    async def create_data_type(
        self, data: Annotated[DataTypeInput, Body]
    ) -> DataTypeOutput:
        try:
            data_type = DataType.create(
                data_type_name=data.data_type_name,
                data_type_info=data.data_type_info
            )
            if data_type is None:
                error_html = RESTAPIError(
                    error="Data type not created",
                    error_description="The data type was not created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return data_type
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the data type"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
