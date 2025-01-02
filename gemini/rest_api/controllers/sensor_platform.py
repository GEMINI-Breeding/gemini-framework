from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.sensor_platform import SensorPlatform
from gemini.rest_api.models import SensorPlatformInput, SensorPlatformOutput, RESTAPIError, JSONB, str_to_dict
from gemini.rest_api.models import SensorOutput
from typing import List, Annotated, Optional

class SensorPlatformController(Controller):

    # Get Sensor Platforms
    @get()
    async def get_sensor_platforms(
        self,
        sensor_platform_name: Optional[str] = None,
        sensor_platform_info: Optional[JSONB] = None
    ) -> List[SensorPlatformOutput]:
        try:

            if sensor_platform_info is not None:
                sensor_platform_info = str_to_dict(sensor_platform_info)

            sensor_platforms = SensorPlatform.search(
                sensor_platform_name=sensor_platform_name,
                sensor_platform_info=sensor_platform_info
            )

            if sensor_platforms is None:
                error_html = RESTAPIError(
                    error="No sensor platforms found",
                    error_description="No sensor platforms were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return sensor_platforms
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving sensor platforms"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
            
    # Get Sensor Platform by ID
    @get(path="/id/{sensor_platform_id:str}")
    async def get_sensor_platform_by_id(
        self, sensor_platform_id: str
    ) -> SensorPlatformOutput:
        try:
            sensor_platform = SensorPlatform.get_by_id(id=sensor_platform_id)
            if sensor_platform is None:
                error_html = RESTAPIError(
                    error="Sensor platform not found",
                    error_description="The sensor platform with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return sensor_platform
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving sensor platforms"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Create Sensor Platform
    @post()
    async def create_sensor_platform(
        self,
        data: Annotated[SensorPlatformInput, Body]
    ) -> SensorPlatformOutput:
        try:
            sensor_platform = SensorPlatform.create(
                sensor_platform_name=data.sensor_platform_name,
                sensor_platform_info=data.sensor_platform_info
            )
            if sensor_platform is None:
                error_html = RESTAPIError(
                    error="Sensor platform not created",
                    error_description="The sensor platform was not created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return sensor_platform
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the sensor platform"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Update Sensor Platform
    @patch(path="/id/{sensor_platform_id:str}")
    async def update_sensor_platform(
        self,
        sensor_platform_id: str,
        data: Annotated[SensorPlatformInput, Body]
    ) -> SensorPlatformOutput:
        try:
            sensor_platform = SensorPlatform.get_by_id(id=sensor_platform_id)
            if sensor_platform is None:
                error_html = RESTAPIError(
                    error="Sensor platform not found",
                    error_description="The sensor platform with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            parameters = data.model_dump()
            sensor_platform = sensor_platform.update(**parameters)
            return sensor_platform
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the sensor platform"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Delete Sensor Platform
    @delete(path="/id/{sensor_platform_id:str}")
    async def delete_sensor_platform(
        self, sensor_platform_id: str
    ) -> None:
        try:
            sensor_platform = SensorPlatform.get_by_id(id=sensor_platform_id)
            if sensor_platform is None:
                error_html = RESTAPIError(
                    error="Sensor platform not found",
                    error_description="The sensor platform with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            sensor_platform.delete()
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the sensor platform"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    
    # Get Sensors for Sensor Platform
    @get(path="/id/{sensor_platform_id:str}/sensors")
    async def get_sensors_for_sensor_platform(
        self, sensor_platform_id: str
    ) -> List[SensorOutput]:
        try:
            sensor_platform = SensorPlatform.get_by_id(id=sensor_platform_id)
            if sensor_platform is None:
                error_html = RESTAPIError(
                    error="Sensor platform not found",
                    error_description="The sensor platform with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            sensors = sensor_platform.get_sensors()
            return sensors
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving sensors"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)

