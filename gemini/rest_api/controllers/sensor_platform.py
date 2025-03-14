from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.sensor_platform import SensorPlatform
from gemini.api.enums import GEMINISensorType, GEMINIDataFormat, GEMINIDataType
from gemini.rest_api.models import SensorPlatformInput, SensorPlatformOutput, SensorPlatformUpdate, RESTAPIError, JSONB, str_to_dict
from gemini.rest_api.models import SensorOutput, SensorInput
from typing import List, Annotated, Optional

class SensorPlatformController(Controller):

    # Get Sensor Platforms
    @get()
    async def get_sensor_platforms(
        self,
        sensor_platform_name: Optional[str] = None,
        sensor_platform_info: Optional[JSONB] = None,
        experiment_name: Optional[str] = 'Experiment A'
    ) -> List[SensorPlatformOutput]:
        try:
            if sensor_platform_info is not None:
                sensor_platform_info = str_to_dict(sensor_platform_info)

            sensor_platforms = SensorPlatform.search(
                sensor_platform_name=sensor_platform_name,
                sensor_platform_info=sensor_platform_info,
                experiment_name=experiment_name
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
                sensor_platform_info=data.sensor_platform_info,
                experiment_name=data.experiment_name
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
        data: Annotated[SensorPlatformUpdate, Body]
    ) -> SensorPlatformOutput:
        try:
            sensor_platform = SensorPlatform.get_by_id(id=sensor_platform_id)
            if sensor_platform is None:
                error_html = RESTAPIError(
                    error="Sensor platform not found",
                    error_description="The sensor platform with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            sensor_platform = sensor_platform.update(
                sensor_platform_name=data.sensor_platform_name,
                sensor_platform_info=data.sensor_platform_info
            )
            if not sensor_platform:
                error_html = RESTAPIError(
                    error="Sensor platform not updated",
                    error_description="The sensor platform was not updated"
                ).to_html()
                return Response(content=error_html, status_code=500)
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
            is_deleted = sensor_platform.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Sensor platform not deleted",
                    error_description="The sensor platform was not deleted"
                ).to_html()
                return Response(content=error_html, status_code=500)
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
            if sensors is None:
                error_html = RESTAPIError(
                    error="No sensors found",
                    error_description="No sensors were found for the given sensor platform"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return sensors
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving sensors"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Add Sensor to Sensor Platform
    @post(path="/id/{sensor_platform_id:str}/sensors")
    async def add_sensor_to_sensor_platform(
        self,
        sensor_platform_id: str,
        data: Annotated[SensorInput, Body]
    ) -> SensorOutput:
        try:
            sensor_platform = SensorPlatform.get_by_id(id=sensor_platform_id)
            if sensor_platform is None:
                error_html = RESTAPIError(
                    error="Sensor platform not found",
                    error_description="The sensor platform with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            sensor = sensor_platform.add_sensor(
                sensor_name=data.sensor_name,
                sensor_type=GEMINISensorType(data.sensor_type_id),
                sensor_data_type=GEMINIDataType(data.sensor_data_type_id),
                sensor_data_format=GEMINIDataFormat(data.sensor_data_format_id),
                sensor_info=data.sensor_info,
                experiment_name=data.experiment_name
            )
            if sensor is None:
                error_html = RESTAPIError(
                    error="Sensor not added",
                    error_description="The sensor was not added to the sensor platform"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return sensor
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while adding the sensor to the sensor platform"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
