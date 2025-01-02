from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.sensor import Sensor
from gemini.api.enums import GEMINISensorType, GEMINIDataType, GEMINIDataFormat
from gemini.rest_api.models import SensorInput, SensorOutput, SensorUpdate, RESTAPIError, JSONB, str_to_dict

from typing import List, Annotated, Optional

class SensorController(Controller):

    # Get Sensors
    @get()
    async def get_sensors(
        self,
        sensor_name: Optional[str] = None,
        sensor_type_id: Optional[int] = None,
        sensor_data_type_id: Optional[int] = None,
        sensor_data_format_id: Optional[int] = None,
        sensor_info: Optional[JSONB] = None,
        experiment_name: Optional[str] = 'Default'
    ) -> List[SensorOutput]:
        try:
            if sensor_info is not None:
                sensor_info = str_to_dict(sensor_info)

            sensors = Sensor.search(
                sensor_name=sensor_name,
                sensor_type_id=sensor_type_id,
                sensor_data_type_id=sensor_data_type_id,
                sensor_data_format_id=sensor_data_format_id,
                sensor_info=sensor_info,
                experiment_name=experiment_name
            )
            if sensors is None:
                error_html = RESTAPIError(
                    error="No sensors found",
                    error_description="No sensors were found with the given search criteria"
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
        

    # Get Sensor by ID
    @get(path="/id/{sensor_id:str}")
    async def get_sensor_by_id(
        self, sensor_id: str
    ) -> SensorOutput:
        try:
            sensor = Sensor.get_by_id(id=sensor_id)
            if sensor is None:
                error_html = RESTAPIError(
                    error="Sensor not found",
                    error_description="The sensor with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return sensor
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving sensor"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Create a new Sensor
    @post()
    async def create_sensor(
        self,
        data: Annotated[SensorInput, Body]
    ) -> SensorOutput:
        try:
            sensor = Sensor.create(
                sensor_name=data.sensor_name,
                sensor_type_id=data.sensor_type_id,
                sensor_data_type_id=data.sensor_data_type_id,
                sensor_data_format_id=data.sensor_data_format_id,
                sensor_info=data.sensor_info,
                experiment_name=data.experiment_name
            )
            if sensor is None:
                error_html = RESTAPIError(
                    error="Failed to create sensor",
                    error_description="An error occurred while creating the sensor"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return sensor
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating sensor"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Update Sensor
    @patch(path="/id/{sensor_id:str}")
    async def update_sensor(
        self,
        sensor_id: str,
        data: Annotated[SensorUpdate, Body]
    ) -> SensorOutput:
        try:
            sensor = Sensor.get_by_id(id=sensor_id)
            if sensor is None:
                error_html = RESTAPIError(
                    error="Sensor not found",
                    error_description="The sensor with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            parameters = data.model_dump()
            sensor = sensor.update(**parameters)
            return sensor
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating sensor"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Delete Sensor
    @delete(path="/id/{sensor_id:str}")
    async def delete_sensor(
        self, sensor_id: str
    ) -> None:
        try:
            sensor = Sensor.get_by_id(id=sensor_id)
            if sensor is None:
                error_html = RESTAPIError(
                    error="Sensor not found",
                    error_description="The sensor with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            sensor.delete()
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting sensor"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)