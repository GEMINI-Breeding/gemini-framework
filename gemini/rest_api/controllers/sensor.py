from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller
from litestar.response import Stream
from litestar.serialization import encode_json

from pydantic import BaseModel

from collections.abc import AsyncGenerator, Generator

from gemini.api.sensor import Sensor
from gemini.api.sensor_record import SensorRecord
from gemini.api.enums import GEMINISensorType, GEMINIDataType, GEMINIDataFormat
from gemini.rest_api.models import SensorInput, SensorOutput, SensorUpdate, RESTAPIError, JSONB, str_to_dict
from gemini.rest_api.models import DatasetOutput
from typing import List, Annotated, Optional

async def sensor_records_bytes_generator(sensor_record_generator: Generator[SensorOutput, None, None]) -> AsyncGenerator[bytes, None]:
    for record in sensor_record_generator:
        record = record.model_dump(exclude_none=True)
        record = encode_json(record) + b'\n'
        yield record


class SensorDatasetInput(BaseModel):
    dataset_name: str
    dataset_info: Optional[JSONB] = None
    collection_date: Optional[str] = None
    experiment_name: Optional[str] = 'Experiment A'


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
        experiment_name: Optional[str] = 'Experiment A'
    ) -> List[SensorOutput]:
        try:
            if sensor_info is not None:
                sensor_info = str_to_dict(sensor_info)

            sensors = Sensor.search(
                sensor_name=sensor_name,
                sensor_type=GEMINISensorType(sensor_type_id) if sensor_type_id else None,
                sensor_data_type=GEMINIDataType(sensor_data_type_id) if sensor_data_type_id else None,
                sensor_data_format=GEMINIDataFormat(sensor_data_format_id) if sensor_data_format_id else None,
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
                sensor_type=GEMINISensorType(data.sensor_type_id) if data.sensor_type_id else None,
                sensor_data_type=GEMINIDataType(data.sensor_data_type_id) if data.sensor_data_type_id else None,
                sensor_data_format=GEMINIDataFormat(data.sensor_data_format_id) if data.sensor_data_format_id else None,
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
            sensor = sensor.update(
                sensor_name=data.sensor_name,
                sensor_type=GEMINISensorType(data.sensor_type_id),
                sensor_data_type=GEMINIDataType(data.sensor_data_type_id),
                sensor_data_format=GEMINIDataFormat(data.sensor_data_format_id),
                sensor_info=data.sensor_info,
            )
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
            is_deleted = sensor.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Failed to delete sensor",
                    error_description="An error occurred while deleting the sensor"
                ).to_html()
                return Response(content=error_html, status_code=500)
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting sensor"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Sensor Datasets
    @get(path="/id/{sensor_id:str}/datasets")
    async def get_sensor_datasets(
        self, sensor_id: str
    ) -> List[DatasetOutput]:
        try:
            sensor = Sensor.get_by_id(id=sensor_id)
            if sensor is None:
                error_html = RESTAPIError(
                    error="Sensor not found",
                    error_description="The sensor with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            datasets = sensor.get_datasets()
            if datasets is None:
                error_html = RESTAPIError(
                    error="No datasets found",
                    error_description="No datasets were found for the given sensor"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return datasets
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving sensor datasets"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)

    # Create a new Sensor Dataset
    @post(path="/id/{sensor_id:str}/datasets")
    async def create_sensor_dataset(
        self,
        sensor_id: str,
        data: Annotated[SensorDatasetInput, Body]
    ) -> DatasetOutput:
        try:
            sensor = Sensor.get_by_id(id=sensor_id)
            if sensor is None:
                error_html = RESTAPIError(
                    error="Sensor not found",
                    error_description="The sensor with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            dataset = sensor.create_dataset(
                dataset_name=data.dataset_name,
                dataset_info=data.dataset_info,
                collection_date=data.collection_date,
                experiment_name=data.experiment_name
            )
            if dataset is None:
                error_html = RESTAPIError(
                    error="Failed to create dataset",
                    error_description="An error occurred while creating the dataset"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return dataset
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating sensor dataset"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Search Sensor Records
    @get(path="/id/{sensor_id:str}/records")
    async def search_sensor_records(
        self,
        sensor_id: str,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None,
        plot_number: Optional[int] = None,
        plot_row_number: Optional[int] = None,
        plot_column_number: Optional[int] = None,
        collection_date: Optional[str] = None
    ) -> Stream:
        try:
            sensor = Sensor.get_by_id(id=sensor_id)
            if sensor is None:
                error_html = RESTAPIError(
                    error="Sensor not found",
                    error_description="The sensor with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            sensor_record_generator = sensor.get_records(
                collection_date=collection_date,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number
            )
            return Stream(sensor_records_bytes_generator(sensor_record_generator))
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving sensor records"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
            
