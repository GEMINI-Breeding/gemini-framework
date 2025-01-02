from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.sensor_type import SensorType
from gemini.rest_api.models import SensorTypeInput, SensorTypeOutput, RESTAPIError, str_to_dict, JSONB

from typing import List, Annotated, Optional

class SensorTypeController(Controller):

    # Get Sensor Types
    @get()
    async def get_sensor_types(
        self,
        sensor_type_name: Optional[str] = None,
        sensor_type_info: Optional[JSONB] = None
    ) -> List[SensorTypeOutput]:
        try:
                
                if sensor_type_info is not None:
                    sensor_type_info = str_to_dict(sensor_type_info)
    
                sensor_types = SensorType.search(
                    sensor_type_name=sensor_type_name,
                    sensor_type_info=sensor_type_info
                )
    
                if sensor_types is None:
                    error_html = RESTAPIError(
                        error="No sensor types found",
                        error_description="No sensor types were found with the given search criteria"
                    ).to_html()
                    return Response(content=error_html, status_code=404)
                return sensor_types
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving sensor types"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Sensor Type by ID
    @get(path="/id/{sensor_type_id:int}")
    async def get_sensor_type_by_id(
         self, sensor_type_id: int
    ) -> SensorTypeOutput:
        try:
            sensor_type = SensorType.get_by_id(id=sensor_type_id)
            if sensor_type is None:
                error_html = RESTAPIError(
                    error="Sensor type not found",
                    error_description="The sensor type with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return sensor_type
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving sensor type"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Create a new Sensor Type
    @post()
    async def create_sensor_type(
        self,
        data: Annotated[SensorTypeInput, Body]
    ) -> SensorTypeOutput:
        try:
            sensor_type = SensorType.create(
                sensor_type_name=data.sensor_type_name,
                sensor_type_info=data.sensor_type_info
            )
            if sensor_type is None:
                error_html = RESTAPIError(
                    error="Sensor type not created",
                    error_description="The sensor type was not created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return sensor_type
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating sensor type"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)