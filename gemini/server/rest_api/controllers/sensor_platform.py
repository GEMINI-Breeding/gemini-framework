from litestar.controller import Controller
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar import Response

from datetime import datetime, date

from gemini.api.sensor_platform import SensorPlatform

from gemini.server.rest_api.src.models import (
    SensorPlatformBase,
    SensorPlatformInput,
    SensorPlatformOutput,
    SensorPlatformSearch,
    SensorOutput,
)

from typing import List, Annotated, Optional


class SensorPlatformController(Controller):

    # Get Sensor Platforms
    @get()
    async def get_sensor_platforms(
        self,
        sensor_platform_name: Optional[str] = None,
        sensor_platform_info: Optional[dict] = None,
    ) -> List[SensorPlatformOutput]:
        try:
            sensor_platforms = SensorPlatform.search(
                sensor_platform_name=sensor_platform_name,
                sensor_platform_info=sensor_platform_info,
            )
            if sensor_platforms is None:
                return Response(content="No sensor platforms found", status_code=404)
            sensor_platforms = [
                sensor_platform.model_dump() for sensor_platform in sensor_platforms
            ]
            sensor_platforms = [
                SensorPlatformOutput.model_validate(sensor_platform)
                for sensor_platform in sensor_platforms
            ]
            return sensor_platforms
        except Exception as e:
            return Response(content=str(e), status_code=500)

    # Get Sensor Platforms by ID
    @get(path="/id/{sensor_platform_id:str}")
    async def get_sensor_platform_by_id(
        self, sensor_platform_id: str
    ) -> SensorPlatformOutput:
        try:
            sensor_platform = SensorPlatform.get_by_id(
                id=sensor_platform_id
            )
            if sensor_platform is None:
                return Response(content="Sensor platform not found", status_code=404)
            return SensorPlatformOutput.model_validate(sensor_platform.model_dump())
        except Exception as e:
            return Response(content=str(e), status_code=500)

    # Create a new Sensor Platform
    @post()
    async def create_sensor_platform(
        self, data: Annotated[SensorPlatformInput, Body]
    ) -> SensorPlatform:
        try:
            sensor_platform = SensorPlatform.create(
                sensor_platform_name=data.sensor_platform_name,
                sensor_platform_info=data.sensor_platform_info,
            )
            if sensor_platform is None:
                return Response(
                    content="Failed to create sensor platform", status_code=500
                )
            return SensorPlatformOutput.model_validate(sensor_platform.model_dump())
        except Exception as e:
            return Response(content=str(e), status_code=500)

    # Get Sensor Platform by sensor platform name
    @get("/{sensor_platform_name:str}")
    async def get_sensor_platform(
        self, sensor_platform_name: str
    ) -> SensorPlatformOutput:
        try:
            sensor_platform = SensorPlatform.get(
                sensor_platform_name=sensor_platform_name
            )
            if sensor_platform is None:
                return Response(content="Sensor platform not found", status_code=404)
            return SensorPlatformOutput.model_validate(sensor_platform.model_dump())
        except Exception as e:
            return Response(content=str(e), status_code=500)

    # Get Sensor Platform Info by sensor platform name
    @get("/{sensor_platform_name:str}/info")
    async def get_sensor_platform_info(self, sensor_platform_name: str) -> dict:
        try:
            sensor_platform = SensorPlatform.get(
                sensor_platform_name=sensor_platform_name
            )
            if sensor_platform is None:
                return Response(content="Sensor platform not found", status_code=404)
            return sensor_platform.get_info()
        except Exception as e:
            return Response(content=str(e), status_code=500)

    # Set Sensor Platform Info by sensor platform name
    @patch("/{sensor_platform_name:str}/info")
    async def set_sensor_platform_info(
        self, sensor_platform_name: str, data: dict
    ) -> dict:
        try:
            sensor_platform = SensorPlatform.get(
                sensor_platform_name=sensor_platform_name
            )
            if sensor_platform is None:
                return Response(content="Sensor platform not found", status_code=404)
            sensor_platform.set_info(sensor_platform_info=data)
            return sensor_platform.get_info()
        except Exception as e:
            return Response(content=str(e), status_code=500)

    # Get All Sensors for a Sensor Platform
    # @get('/{sensor_platform_name:str}/sensors')
    @get("/{sensor_platform_name:str}/sensors")
    async def get_sensor_platform_sensors(
        self, sensor_platform_name: str = "Default"
    ) -> List[SensorOutput]:
        try:
            sensor_platform = SensorPlatform.get(
                sensor_platform_name=sensor_platform_name
            )
            if sensor_platform is None:
                return Response(content="Sensor platform not found", status_code=404)
            sensors = sensor_platform.get_sensors()
            if sensors is None:
                return Response(content="No sensors found", status_code=404)
            sensors = [sensor.model_dump() for sensor in sensors]
            sensors = [
                SensorOutput.model_validate(sensor) for sensor in sensors
            ]
            return sensors
        except Exception as e:
            return Response(content=str(e), status_code=500)

    # Add Existing Sensor to Sensor Platform
    @patch("/{sensor_platform_name:str}/sensors/add")
    async def add_sensor_to_platform(
        self, sensor_platform_name: str, sensor_name: str
    ) -> SensorPlatformOutput:
        try:
            sensor_platform = SensorPlatform.get(
                sensor_platform_name=sensor_platform_name
            )
            if sensor_platform is None:
                return Response(content="Sensor platform not found", status_code=404)
            sensor_platform.add_sensor(sensor_name=sensor_name)
            return SensorPlatformOutput.model_validate(sensor_platform.model_dump())
        except Exception as e:
            return Response(content=str(e), status_code=500)

    # Remove Existing Sensor from Sensor Platform
    @patch("/{sensor_platform_name:str}/sensors/remove")
    async def remove_sensor_from_platform(
        self, sensor_platform_name: str, sensor_name: str
    ) -> SensorPlatformOutput:
        try:
            sensor_platform = SensorPlatform.get(
                sensor_platform_name=sensor_platform_name
            )
            if sensor_platform is None:
                return Response(content="Sensor platform not found", status_code=404)
            sensor_platform.remove_sensor(sensor_name=sensor_name)
            return SensorPlatformOutput.model_validate(sensor_platform.model_dump())
        except Exception as e:
            return Response(content=str(e), status_code=500)
    
