from litestar.controller import Controller
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import get, post, patch, delete, put
from litestar.params import Body
from litestar.response import Stream
from litestar.serialization import encode_json
from litestar import Response

from datetime import datetime, date
from collections.abc import AsyncGenerator
from asyncio import sleep

from gemini.api.sensor import Sensor
from gemini.api.sensor_record import SensorRecord
from gemini.rest_api.src.models import (
    SensorRecordBase,
    SensorRecordInput,
    SensorRecordOutput,
    SensorRecordSearch,
    SensorOutput
)

from gemini.models import SensorRecordsIMMVModel
from gemini.rest_api.src.file_handler import file_handler
from gemini.object_store import storage_service

from typing import List, Annotated, Optional

async def sensor_record_search_generator(search_parameters: SensorRecordSearch) -> AsyncGenerator[bytes, None]:
    
    record_info = search_parameters.record_info or {}
    record_info.update({
        "experiment_name": search_parameters.experiment_name,
        "season_name": search_parameters.season_name,
        "site_name": search_parameters.site_name,
        "plot_number": search_parameters.plot_number,
        "plot_row_number": search_parameters.plot_row_number,
        "plot_column_number": search_parameters.plot_column_number
    })
    record_info = {k: v for k, v in record_info.items() if v is not None}
    search_parameters.record_info = record_info
    search_parameters = search_parameters.model_dump(exclude_none=True)

    for record in SensorRecordsIMMVModel.stream_raw(**search_parameters):
        record = SensorRecord.get_by_id(id=record)
        record = record.model_dump(exclude_none=True)
        yield encode_json(record)



class SensorRecordController(Controller):

    # Get Sensor Records
    @get()
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
            
            sensor = Sensor.get(sensor_name)
            if not sensor:
                return Response(content="Sensor not found", status_code=404)

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
            return Stream(sensor_record_search_generator(search_parameters))
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Create Sensor Record
    @post()
    async def create_sensor_record(
        self,
        data: Annotated[SensorRecordInput, Body(media_type=RequestEncodingType.MULTI_PART)]
    ) -> SensorRecordOutput:
        try:
            sensor = Sensor.get(data.sensor_name)
            if not sensor:
                return Response(content="Sensor not found", status_code=404)
            
            if data.sensor_data is None and data.file is None:
                return Response(content="Sensor data or file is required", status_code=400)
            
            if data.file:
                local_file_path = await file_handler.create_file(data.file)
                sensor_data = data.sensor_data or {}
                sensor_data.update({"file": local_file_path})
                data.sensor_data = sensor_data


            record = sensor.add_record(
                sensor_data=data.sensor_data,
                experiment_name=data.experiment_name,
                timestamp=data.timestamp,
                collection_date=data.collection_date,
                dataset_name=data.dataset_name,
                season_name=data.season_name,
                site_name=data.site_name,
                plot_number=data.plot_number,
                plot_row_number=data.plot_row_number,
                plot_column_number=data.plot_column_number,
                record_info=data.record_info
            )

            if not record:
                return Response(content="Failed to create sensor record", status_code=500)

            record = record.model_dump(exclude_none=True)
            return SensorRecordOutput.model_validate(record)
        except Exception as e:
            return Response(content=str(e), status_code=500)


    # Get Download URI by Record ID
    @get('/{record_id:str}/download')
    async def get_download_uri(
        self,
        record_id: str
    ) -> str:
        try:
            record = SensorRecord.get_by_id(record_id)
            if not record:
                return Response(content="Record not found", status_code=404)
            # Check if record has file_uri
            download_url = record.get_download_uri()
            if not download_url:
                return Response(content="No file URI found in sensor data", status_code=400)
            return download_url
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Sensor Record by Record ID
    @get('/{record_id:str}')
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
    @get('/{record_id:str}/info')
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
    @patch('/{record_id:str}/info')
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
    @delete('/{record_id:str}')
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
