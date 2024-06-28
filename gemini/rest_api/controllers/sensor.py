from litestar.controller import Controller             
from litestar.handlers import get, post, put, delete, patch
from litestar.params import Body
from litestar import Response

from gemini.api.sensor import Sensor
from gemini.api.enums import GEMINISensorType, GEMINIDataType, GEMINIDataFormat
from gemini.rest_api.worker import task_queue
from gemini.rest_api.src.models import (
    SensorBase,
    SensorInput,
    SensorOutput,
    DatasetOutput
)

from typing import List, Optional, Any, Annotated



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
        experiment_name: Optional[str] = 'Default'
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
    @patch('/{sensor_name:str}/info')
    async def set_sensor_info(
        self,
        sensor_name: str,
        data: dict
    ) -> dict:
        try:
            sensor = Sensor.get(sensor_name)
            if not sensor:
                return Response(content="Sensor not found", status_code=404)
            sensor.set_info(data)
            return sensor.get_info()
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
        
    
    # Test Task Queue
    @get('/test')
    async def test_task_queue(self) -> dict:
        try:
            job = await task_queue.enqueue("get_system_time", timeout=0)
            job_info = job.to_dict()
            return job_info
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    