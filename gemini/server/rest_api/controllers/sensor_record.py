from litestar.controller import Controller
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.response import Stream
from litestar.enums import RequestEncodingType
from litestar import Response, Request

from datetime import date
from collections.abc import AsyncGenerator

from gemini.api.sensor import Sensor
from gemini.api.sensor_record import SensorRecord
from gemini.server.rest_api.src.models import (
    SensorRecordInput,
    SensorRecordOutput,
    SensorRecordsPaginatedOutput,
    SensorRecordSearch
)

from gemini.server.database.models import SensorRecordsIMMVModel

from typing import List, Annotated, Optional

async def sensor_record_search_generator(search_parameters: SensorRecordSearch) -> AsyncGenerator[SensorRecordOutput, None]:  
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
        record = SensorRecord.get_by_id(record_id=record)
        record = record.model_dump_json(exclude_none=True)
        record = record + '\n'
        yield record



class SensorRecordController(Controller):

    # Get Sensor Records
    @get()
    async def get_sensor_records(
        self,
        sensor_name: str,
        sensor_id: Optional[str] = None,
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
            
            # Check if sensor_id is provided
            if sensor_id:
                sensor = Sensor.get_by_id(sensor_id)
            elif sensor_name:
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
            return Stream(sensor_record_search_generator(search_parameters), media_type='application/ndjson')
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # # Get Paginated Sensor Records
    # @get('/paginate', name='get_paginated_sensor_records')
    # async def get_paginated_sensor_records(
    #     self,
    #     request: Request,
    #     sensor_name: str,
    #     sensor_id: Optional[str] = None,
    #     collection_date: Optional[date] = None,
    #     experiment_name: Optional[str] = None,
    #     season_name: Optional[str] = None,
    #     site_name: Optional[str] = None,
    #     plot_number: Optional[int] = None,
    #     plot_row_number: Optional[int] = None,
    #     plot_column_number: Optional[int] = None,
    #     record_info: Optional[dict] = None,
    #     order_by: Optional[str] = 'timestamp',
    #     page_number: Optional[int] = 1,
    #     page_limit: Optional[int] = 50
    # ) -> List[SensorRecordsPaginatedOutput]:
    #     try:
    #         # Check if sensor_id is provided
    #         if sensor_id:
    #             sensor = Sensor.get_by_id(sensor_id)
    #         elif sensor_name:
    #             sensor = Sensor.get(sensor_name)
                
    #         if not sensor:
    #             return Response(content="Sensor not found", status_code=404)


    #         search_parameters = SensorRecordSearch(
    #             sensor_name=sensor_name,
    #             collection_date=collection_date,
    #             experiment_name=experiment_name,
    #             season_name=season_name,
    #             site_name=site_name,
    #             plot_number=plot_number,
    #             plot_row_number=plot_row_number,
    #             plot_column_number=plot_column_number,
    #             record_info=record_info
    #         )
            
    #         search_parameters = search_parameters.model_dump(exclude_none=True)
            
    #         number_of_records, number_of_pages, records = SensorRecordsIMMVModel.paginate(
    #             order_by=order_by,
    #             page_number=page_number,
    #             page_limit=page_limit,
    #             **search_parameters
    #         )

    #         # Generate URLs for next and previous pages
    #         previous_page_url, next_page_url = self.generate_pagination_urls(request, page_number, number_of_pages)

    #         # Convert records to SensorRecordOutput
    #         records = [SensorRecordOutput.model_validate(record) for record in records]

    #         # Dump records to dict
    #         records = [record.model_dump(exclude_none=True) for record in records]


    #         paginated_response = SensorRecordsPaginatedOutput(
    #             total_records=number_of_records,
    #             total_pages=number_of_pages,
    #             current_page=page_number,
    #             page_limit=page_limit,
    #             previous_page=None if page_number == 1 else previous_page_url,
    #             next_page=None if page_number == number_of_pages else next_page_url,
    #             records = records,
    #         )
            
    #         return SensorRecordsPaginatedOutput.model_validate(paginated_response)
            
    #     except Exception as e:
    #         return Response(content=str(e), status_code=500)

    # Create Sensor Record
    # @post()
    # async def create_sensor_record(
    #     self,
    #     data: Annotated[SensorRecordInput, Body(media_type=RequestEncodingType.MULTI_PART)]
    # ) -> SensorRecordOutput:
    #     try:
    #         sensor = Sensor.get(data.sensor_name)
    #         if not sensor:
    #             return Response(content="Sensor not found", status_code=404)
            
    #         if data.sensor_data is None and data.file is None:
    #             return Response(content="Sensor data or file is required", status_code=400)
            
    #         # if data.file:
    #         #     local_file_path = await file_handler.create_file(data.file)
    #         #     sensor_data = data.sensor_data or {}
    #         #     sensor_data.update({"file": local_file_path})
    #         #     data.sensor_data = sensor_data


    #         record = sensor.add_record(
    #             sensor_data=data.sensor_data,
    #             experiment_name=data.experiment_name,
    #             timestamp=data.timestamp,
    #             collection_date=data.collection_date,
    #             dataset_name=data.dataset_name,
    #             season_name=data.season_name,
    #             site_name=data.site_name,
    #             plot_number=data.plot_number,
    #             plot_row_number=data.plot_row_number,
    #             plot_column_number=data.plot_column_number,
    #             record_info=data.record_info
    #         )

    #         if not record:
    #             return Response(content="Failed to create sensor record", status_code=500)

    #         record = record.model_dump(exclude_none=True)
    #         return SensorRecordOutput.model_validate(record)
    #     except Exception as e:
    #         return Response(content=str(e), status_code=500)


    # # Get Download URI by Record ID
    # @get('/{record_id:str}/download')
    # async def get_download_uri(
    #     self,
    #     record_id: str
    # ) -> str:
    #     try:
    #         record = SensorRecord.get_by_id(record_id)
    #         if not record:
    #             return Response(content="Record not found", status_code=404)
    #         # Check if record has file_uri
    #         download_url = record.get_download_uri()
    #         if not download_url:
    #             return Response(content="No file URI found in sensor data", status_code=400)
    #         return download_url
    #     except Exception as e:
    #         return Response(content=str(e), status_code=500)
        
    # # Get Sensor Record by Record ID
    # @get('/{record_id:str}')
    # async def get_sensor_record(
    #     self,
    #     record_id: str
    # ) -> SensorRecordOutput:
    #     try:
    #         record = SensorRecord.get_by_id(record_id)
    #         if not record:
    #             return Response(content="Record not found", status_code=404)
    #         return SensorRecordOutput.model_validate(record.model_dump(exclude_none=True))
    #     except Exception as e:
    #         return Response(content=str(e), status_code=500)
        
    # Get Sensor Record Info by Record ID
    # @get('/{record_id:str}/info')
    # async def get_sensor_record_info(
    #     self,
    #     record_id: str
    # ) -> dict:
    #     try:
    #         record = SensorRecord.get_by_id(record_id)
    #         if not record:
    #             return Response(content="Record not found", status_code=404)
    #         return record.get_info()
    #     except Exception as e:
    #         return Response(content=str(e), status_code=500)
        
    # # Set Sensor Record Info by Record ID
    # @patch('/{record_id:str}/info')
    # async def set_sensor_record_info(
    #     self,
    #     record_id: str,
    #     data: dict
    # ) -> dict:
    #     try:
    #         record = SensorRecord.get_by_id(record_id)
    #         if not record:
    #             return Response(content="Record not found", status_code=404)
    #         return record.set_info(data)
    #     except Exception as e:
    #         return Response(content=str(e), status_code=500)
        
    # # Delete Sensor Record by Record ID
    # @delete('/{record_id:str}')
    # async def delete_sensor_record(
    #     self,
    #     record_id: str
    # ) -> None:
    #     try:
    #         record = SensorRecord.get_by_id(record_id)
    #         if not record:
    #             return Response(content="Record not found", status_code=404)
    #         sucess_deleted = record.delete()
    #         if not sucess_deleted:
    #             return Response(content="Record could not be deleted", status_code=500)
    #         return None
    #     except Exception as e:
    #         return Response(content=str(e), status_code=500)
        

    # # Utility function for generating pagination URLs
    # def generate_pagination_urls(self, request, page_number, number_of_pages):
    #     request_args = dict(request.query_params.items())# Make a copy to avoid modifying the original
    #     previous_page_url = None
    #     next_page_url = None

    #     if page_number > 1:
    #         previous_page_number = page_number - 1
    #         request_args['page_number'] = previous_page_number
    #         previous_page_url = request.url_for(
    #             'get_paginated_sensor_records'
    #         )
    #         query_string = '&'.join([f'{k}={v}' for k, v in request_args.items()])
    #         previous_page_url = f'{previous_page_url}?{query_string}'

    #     if page_number < number_of_pages:
    #         next_page_number = page_number + 1
    #         request_args['page_number'] = next_page_number
    #         next_page_url = request.url_for(
    #             'get_paginated_sensor_records',
    #         )
    #         query_string = '&'.join([f'{k}={v}' for k, v in request_args.items()])
    #         next_page_url = f'{next_page_url}?{query_string}'

    #     return previous_page_url, next_page_url
        

