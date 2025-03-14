from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.data_type import DataType
from gemini.rest_api.models import (
    DataTypeInput, 
    DataTypeOutput,
    DataTypeUpdate,
    DataFormatOutput,
    DataFormatInput,
    RESTAPIError, 
    JSONB, 
    str_to_dict
)

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
        
    # Create a new Data Type
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
        

    # Update Data Type
    @patch(path="/id/{data_type_id:int}")
    async def update_data_type(
        cls, data_type_id: int, data: Annotated[DataTypeUpdate, Body]
    ) -> DataTypeOutput:
        try:
            data_type = DataType.get_by_id(id=data_type_id)
            if data_type is None:
                error_html = RESTAPIError(
                    error="Data type not found",
                    error_description="The data type with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            data_type = data_type.update(
                data_type_name=data.data_type_name,
                data_type_info=data.data_type_info
            )
            if data_type is None:
                error_html = RESTAPIError(
                    error="Data type update failed",
                    error_description="The data type was not updated"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return data_type
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the data type"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Delete Data Type
    @delete(path="/id/{data_type_id:int}")
    async def delete_data_type(
        cls, data_type_id: int
    ) -> None:
        try:
            data_type = DataType.get_by_id(id=data_type_id)
            if data_type is None:
                error_html = RESTAPIError(
                    error="Data type not found",
                    error_description="The data type with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = data_type.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Data type not deleted",
                    error_description="The data type could not be deleted"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return None
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the data type"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Formats
    @get(path="/id/{data_type_id:int}/formats")
    async def get_data_type_formats(
        self, data_type_id: int
    ) -> List[DataFormatOutput]:
        try:
            data_type = DataType.get_by_id(id=data_type_id)
            if data_type is None:
                error_html = RESTAPIError(
                    error="Data type not found",
                    error_description="The data type with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            data_formats = data_type.get_formats()
            if data_formats is None:
                error_html = RESTAPIError(
                    error="No data formats found",
                    error_description="No data formats were found for the given data type"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return data_formats
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving data formats"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Add Format
    @post(path="/id/{data_type_id:int}/formats")
    async def add_data_type_format(
        self, data_type_id: int, data: Annotated[DataFormatInput, Body]
    ) -> DataFormatOutput:
        try:
            data_type = DataType.get_by_id(id=data_type_id)
            if data_type is None:
                error_html = RESTAPIError(
                    error="Data type not found",
                    error_description="The data type with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            data_format = data_type.create_format(
                data_format_name=data.data_format_name,
                data_format_mime_type=data.data_format_mime_type,
                data_format_info=data.data_format_info
            )
            if data_format is None:
                error_html = RESTAPIError(
                    error="Data format not created",
                    error_description="The data format was not created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return data_format
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the data format"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
            
