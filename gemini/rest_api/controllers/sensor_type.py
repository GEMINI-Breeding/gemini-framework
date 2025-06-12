from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.sensor_type import SensorType
from gemini.rest_api.models import SensorTypeInput, SensorTypeOutput, SensorTypeUpdate, RESTAPIError, str_to_dict, JSONB

from typing import List, Annotated, Optional

class SensorTypeController(Controller):

    # Get All Sensor Types
    @get(path="/all")
    async def get_all_sensor_types(self) -> List[SensorTypeOutput]:
        try:
            sensor_types = SensorType.get_all()
            if sensor_types is None:
                error = RESTAPIError(
                    error="No sensor types found",
                    error_description="No sensor types were found"
                )
                return Response(content=error, status_code=404)
            return sensor_types
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving all sensor types"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)

    # Get all Sensor Types
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
                error = RESTAPIError(
                    error="No sensor types found",
                    error_description="No sensor types were found with the given search criteria"
                )
                return Response(content=error, status_code=404)
            return sensor_types
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving sensor types"
            )
            return Response(content=error_message, status_code=500)
        
    # Get Sensor Type by ID
    @get(path="/id/{sensor_type_id:int}")
    async def get_sensor_type_by_id(
            self, sensor_type_id: int
        ) -> SensorTypeOutput:
            try:
                sensor_type = SensorType.get_by_id(id=sensor_type_id)
                if sensor_type is None:
                    error = RESTAPIError(
                        error="Sensor type not found",
                        error_description="The sensor type with the given ID was not found"
                    )
                    return Response(content=error, status_code=404)
                return sensor_type
            except Exception as e:
                error_message = RESTAPIError(
                    error=str(e),
                    error_description="An error occurred while retrieving sensor type"
                )
                return Response(content=error_message, status_code=500)
            
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
                error = RESTAPIError(
                    error="Sensor type not created",
                    error_description="The sensor type was not created"
                )
                return Response(content=error, status_code=500)
            return sensor_type
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating sensor type"
            )
            return Response(content=error_message, status_code=500)

    # Update a Sensor Type
    @patch(path="/id/{sensor_type_id:int}")
    async def update_sensor_type(
        self,
        sensor_type_id: int,
        data: Annotated[SensorTypeUpdate, Body]
    ) -> SensorTypeOutput:
        try:
            sensor_type = SensorType.get_by_id(id=sensor_type_id)
            if sensor_type is None:
                error = RESTAPIError(
                    error="Sensor type not found",
                    error_description="The sensor type with the given ID was not found"
                )
                return Response(content=error, status_code=404)
            sensor_type = sensor_type.update(
                sensor_type_name=data.sensor_type_name,
                sensor_type_info=data.sensor_type_info
            )
            if sensor_type is None:
                error = RESTAPIError(
                    error="Sensor type not updated",
                    error_description="The sensor type was not updated"
                )
                return Response(content=error, status_code=500)
            return sensor_type
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating sensor type"
            )
            return Response(content=error_message, status_code=500)
        
    # Delete a Sensor Type
    @delete(path="/id/{sensor_type_id:int}")
    async def delete_sensor_type(
        self,
        sensor_type_id: int
    ) -> None:
        try:
            sensor_type = SensorType.get_by_id(id=sensor_type_id)
            if sensor_type is None:
                error = RESTAPIError(
                    error="Sensor type not found",
                    error_description="The sensor type with the given ID was not found"
                )
                return Response(content=error, status_code=404)
            is_deleted = sensor_type.delete()
            if not is_deleted:
                error = RESTAPIError(
                    error="Sensor type not deleted",
                    error_description="The sensor type was not deleted"
                )
                return Response(content=error, status_code=500)
            return None
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting sensor type"
            )
            return Response(content=error_message, status_code=500)
    