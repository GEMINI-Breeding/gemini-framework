from litestar import Response
from litestar.plugins.pydantic import PydanticDTO
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.data_format import DataFormat
from gemini.rest_api.models import DataFormatInput, DataFormatOutput, RESTAPIError, JSONB, str_to_dict

from typing import List, Annotated, Optional

class DataFormatController(Controller):

    # Get Data Formats
    @get()
    async def get_data_formats(
        self,
        data_format_name: Optional[str] = None,
        data_format_mime_type: Optional[str] = None,
        data_format_info: Optional[JSONB] = None
    ) -> List[DataFormat]:
        try:

            if data_format_info is not None:
                data_format_info = str_to_dict(data_format_info)

            data_formats = DataFormat.search(
                data_format_name=data_format_name,
                data_format_mime_type=data_format_mime_type,
                data_format_info=data_format_info
            )
            if data_formats is None:
                error_html = RESTAPIError(
                    error="No data formats found",
                    error_description="No data formats were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            data_formats = [data_format.model_dump() for data_format in data_formats]
            data_formats = [DataFormatOutput.model_validate(data_format) for data_format in data_formats]
            return data_formats
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving data formats"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Data Format by ID
    @get(path="/id/{data_format_id:int}")
    async def get_data_format_by_id(
        self, data_format_id: int
    ) -> DataFormatOutput:
        try:
            data_format = DataFormat.get_by_id(id=data_format_id)
            if data_format is None:
                error_html = RESTAPIError(
                    error="Data format not found",
                    error_description="The data format with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            data_format = DataFormatOutput.model_validate(data_format.model_dump())
            return data_format
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the data format"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Create a new Data Format
    @post()
    async def create_data_format(
        self, data: Annotated[DataFormatInput, Body]
    ) -> DataFormat:
        try:
            data_format = DataFormat.create(
                data_format_name=data.data_format_name,
                data_format_mime_type=data.data_format_mime_type,
                data_format_info=data.data_format_info
            )
            if data_format is None:
                error_html = RESTAPIError(
                    error="Data format not created",
                    error_description="The data format could not be created"
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
