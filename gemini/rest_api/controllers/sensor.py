from litestar.controller import Controller
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import get, post, put, delete
from litestar.params import Body
from litestar.response import Stream, File
from litestar.serialization import encode_json
from litestar import Response

from datetime import datetime, date
from collections.abc import AsyncGenerator

from gemini.api.sensor import Sensor
from gemini.api.sensor_record import SensorRecord
from gemini.api.sensor_platform import SensorPlatform
from gemini.api.enums import GEMINISensorType, GEMINIDataType, GEMINIDataFormat

from gemini.rest_api.src.models import (
    SensorBase,
    SensorInput,
    SensorOutput,
    SensorSearch,
    SensorRecordInput,
    SensorRecordOutput,
    SensorRecordSearch,
    DatasetOutput
)

from typing import List, Optional, Any, Annotated

async def sensor_record_search_generator(search_parameters: SensorRecordSearch) -> AsyncGenerator[SensorRecordOutput, None]:
    search_parameters = search_parameters.model_dump(exclude_none=True)
    sensor = Sensor.get(search_parameters["sensor_name"])
    
    # Remove sensor_name from search parameters
    search_parameters.pop("sensor_name")
    sensor_records = sensor.get_records(**search_parameters)
    
    for record in sensor_records:
        record = record.model_dump_json(exclude_none=True)
        yield record
        

class SensorController(Controller):
    
    # Get Sensors
    @get()
    async def get_sensors(
        self,
        sensor_name: Optional[str] = None,
        sensor_platform_name: Optional[str] = None,
        sensor_type_id: Optional[GEMINISensorType] = None,
        sensor_data_type_id: Optional[GEMINIDataType] = None,
        sensor_data_format_id: Optional[GEMINIDataFormat] = None,
        sensor_info: Optional[dict] = None,
        experiment_name: Optional[str] = None
    ) -> List[SensorOutput]:
        try:
            sensors = Sensor.search(
                sensor_name=sensor_name,
                experiment_name=experiment_name,
                sensor_platform_name=sensor_platform_name,
                sensor_type=sensor_type_id,
                sensor_data_type=sensor_data_type_id,
                sensor_data_format=sensor_data_format_id,
                sensor_info=sensor_info
            )
            if not sensors:
                return Response(content="No sensors found", status_code=404)
            sensors = [sensor.model_dump(exclude_none=True) for sensor in sensors]
            sensors = [SensorOutput.model_validate(sensor) for sensor in sensors]
            return sensors
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Create A New Sensor
    @post()
    async def create_sensor(
        self,
        data: Annotated[SensorInput, Body]
    ) -> SensorOutput:
        try:
            sensor = Sensor.create(
                sensor_name=data.sensor_name,
                sensor_platform_name=data.sensor_platform_name,
                sensor_type=GEMINISensorType(data.sensor_type_id),
                sensor_data_type=GEMINIDataType(data.sensor_data_type_id),
                sensor_data_format=GEMINIDataFormat(data.sensor_data_format_id),
                sensor_info=data.sensor_info,
                experiment_name=data.experiment_name
            )
            if not sensor:
                return Response(content="Sensor already exists", status_code=400)
            sensor = sensor.model_dump(exclude_none=True)
            return SensorOutput.model_validate(sensor)
        except Exception as e:
            return Response(content=str(e), status_code=500)
            
    
    # Get Sensor by Sensor Type ID
    @get('/type/{sensor_type_id:int}')
    async def get_sensors_by_type(
        self, sensor_type_id: int
    ) -> List[SensorOutput]:
        try:
            sensors = Sensor.get_by_type(GEMINISensorType(sensor_type_id))
            if not sensors:
                return Response(content="No sensors found", status_code=404)
            sensors = [sensor.model_dump(exclude_none=True) for sensor in sensors]
            sensors = [SensorOutput.model_validate(sensor) for sensor in sensors]
            return sensors
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Sensor by Sensor Name
    @get('/{sensor_name:str}')
    async def get_sensor(
        self, sensor_name: str
    ) -> SensorOutput:
        try:
            sensor = Sensor.get(sensor_name)
            if not sensor:
                return Response(content="Sensor not found", status_code=404)
            return SensorOutput.model_validate(sensor.model_dump(exclude_none=True))
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Sensor Info by Sensor Name
    @get('/{sensor_name:str}/info')
    async def get_sensor_info(
        self, sensor_name: str
    ) -> dict:
        try:
            sensor = Sensor.get(sensor_name)
            if not sensor:
                return Response(content="Sensor not found", status_code=404)
            return sensor.get_info()
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Set Sensor Info by Sensor Name
    @put('/{sensor_name:str}/info')
    async def set_sensor_info(
        self,
        sensor_name: str,
        data: dict
    ) -> dict:
        try:
            sensor = Sensor.get(sensor_name)
            if not sensor:
                return Response(content="Sensor not found", status_code=404)
            return sensor.set_info(data)
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Sensor Datasets
    @get('/{sensor_name:str}/datasets')
    async def get_sensor_datasets(
        self, sensor_name: str
    ) -> List[DatasetOutput]:
        try:
            sensor = Sensor.get(sensor_name)
            if not sensor:
                return Response(content="Sensor not found", status_code=404)
            datasets = sensor.get_datasets()
            if not datasets:
                return Response(content="No datasets found", status_code=404)
            datasets = [dataset.model_dump(exclude_none=True) for dataset in datasets]
            datasets = [DatasetOutput.model_validate(dataset) for dataset in datasets]
            return datasets
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Sensor Records
    @get('/{sensor_name:str}/records')
    async def get_sensor_records(
        self,
        sensor_name: str,
        collection_date: Optional[date] = None,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None,
        plot_number: Optional[int] = None,
        plot_row_number: Optional[int] = None,
        plot_column_number: Optional[int] = None,
        record_info: Optional[dict] = None
    ) -> Stream:
        try:
            search_parameters = SensorRecordSearch(
                sensor_name=sensor_name,
                collection_date=collection_date,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                record_info=record_info
            )
            records = Stream(sensor_record_search_generator(search_parameters))
            return records
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Create Sensor Record
    @post('/{sensor_name:str}/records')
    async def create_sensor_record(
        self,
        sensor_name: str,
        data: Annotated[SensorRecordInput, Body]
    ) -> SensorRecordOutput:
        try:
            sensor = Sensor.get(sensor_name)
            if not sensor:
                return Response(content="Sensor not found", status_code=404)
            record = sensor.add_record(
                sensor_data=data.sensor_data,
                timestamp=data.timestamp,
                collection_date=data.collection_date,
                dataset_name=data.dataset_name,
                experiment_name=data.experiment_name,
                season_name=data.season_name,
                site_name=data.site_name,
                plot_number=data.plot_number,
                plot_row_number=data.plot_row_number,
                plot_column_number=data.plot_column_number,
                record_info=data.record_info
            )
            if record is None:
                return Response(content="Record already exists", status_code=400)
            record = record.model_dump(exclude_none=True)
            return SensorRecordOutput.model_validate(record)
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Sensor Record by Record ID
    @get('/records/{record_id:str}')
    async def get_sensor_record(
        self,
        record_id: str
    ) -> SensorRecordOutput:
        try:
            record = SensorRecord.get_by_id(record_id)
            if not record:
                return Response(content="Record not found", status_code=404)
            return SensorRecordOutput.model_validate(record.model_dump(exclude_none=True))
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Sensor Record Info by Record ID
    @get('/records/{record_id:str}/info')
    async def get_sensor_record_info(
        self,
        record_id: str
    ) -> dict:
        try:
            record = SensorRecord.get_by_id(record_id)
            if not record:
                return Response(content="Record not found", status_code=404)
            return record.get_info()
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Set Sensor Record Info by Record ID
    @put('/records/{record_id:str}/info')
    async def set_sensor_record_info(
        self,
        record_id: str,
        data: dict
    ) -> dict:
        try:
            record = SensorRecord.get_by_id(record_id)
            if not record:
                return Response(content="Record not found", status_code=404)
            return record.set_info(data)
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Delete Sensor Record by Record ID
    @delete('/records/{record_id:str}')
    async def delete_sensor_record(
        self,
        record_id: str
    ) -> None:
        try:
            record = SensorRecord.get_by_id(record_id)
            if not record:
                return Response(content="Record not found", status_code=404)
            sucess_deleted = record.delete()
            if not sucess_deleted:
                return Response(content="Record could not be deleted", status_code=500)
            return None
        except Exception as e:
            return Response(content=str(e), status_code=500)