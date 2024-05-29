from collections.abc import AsyncGenerator
from datetime import datetime, date
from typing import Annotated, List, Optional
from uuid import UUID

from litestar import Request
from litestar.controller import Controller
from litestar.dto import DTOConfig, DTOData
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import delete, get, patch, post
from litestar.params import Body
from litestar.response import Stream
from litestar.serialization import default_serializer, encode_json
from pydantic import BaseModel

from gemini.api.sensor import Sensor
from gemini.api.sensor_type import SensorType
from gemini.api.experiment import Experiment
from gemini.api.sensor_platform import SensorPlatform
from gemini.api.data_type import DataType
from gemini.api.data_format import DataFormat
from gemini.api.dataset import Dataset
from gemini.api.script_record import ScriptRecord

from gemini.api.enums import GEMINIDataType, GEMINIDataFormat, GEMINISensorType


async def sensor_generator(**params) -> AsyncGenerator[bytes, None]:
    sensors = Sensor.search(**params)
    for sensor in sensors:
        sensor = sensor.model_dump_json()
        yield sensor


class SensorInput(BaseModel):
    sensor_name: str
    sensor_info: Optional[dict] = {}
    sensor_type: GEMINIDataType = GEMINIDataType.Default
    sensor_data_type: GEMINIDataType = GEMINIDataType.Default
    sensor_platform_name: Optional[str] = None
    experiment_name: Optional[str] = None


class SensorController(Controller):

    # Filter Sensors
    @get()
    async def get_sensors(
        self,
        sensor_name: Optional[str] = None,
        sensor_type: Optional[GEMINIDataType] = None,
        sensor_data_type: Optional[GEMINIDataType] = None,
    ) -> List[Sensor]:
        sensors = Sensor.search(
            sensor_name=sensor_name,
            sensor_type=sensor_type,
            sensor_data_type=sensor_data_type,
        )
        return sensors

    # Get Sensor by name
    @get("/{sensor_name:str}")
    async def get_sensor_by_name(self, sensor_name: str) -> Sensor:
        sensor = Sensor.get_by_name(sensor_name)
        return sensor

    # Get Sensor by ID
    @get("/id/{sensor_id:uuid}")
    async def get_sensor_by_id(self, sensor_id: UUID) -> Sensor:
        sensor = Sensor.get_by_id(sensor_id)
        return sensor

    # Create a new sensor
    @post()
    async def create_sensor(self, sensor_input: Annotated[SensorInput, Body]) -> Sensor:
        sensor = Sensor.create(
            sensor_name=sensor_input.sensor_name,
            sensor_info=sensor_input.sensor_info,
            sensor_type=sensor_input.sensor_type,
            sensor_data_type=sensor_input.sensor_data_type,
            sensor_platform_name=sensor_input.sensor_platform_name,
            experiment_name=sensor_input.experiment_name,
        )
        return sensor

    # Delete a sensor by name
    @delete("/{sensor_name:str}")
    async def delete_sensor_by_name(self, sensor_name: str) -> None:
        sensor = Sensor.get_by_name(sensor_name)
        sensor.delete()

    # Delete a sensor by ID
    @delete("/id/{sensor_id:uuid}")
    async def delete_sensor_by_id(self, sensor_id: UUID) -> None:
        sensor = Sensor.get_by_id(sensor_id)
        sensor.delete()

    # Get sensor info
    @get("/{sensor_name:str}/info")
    async def get_sensor_info(self, sensor_name: str) -> dict:
        sensor = Sensor.get_by_name(sensor_name)
        sensor = sensor.get_info()
        return sensor

    # Set sensor info
    @patch("/{sensor_name:str}/info")
    async def set_sensor_info(
        self, sensor_name: str, info: Annotated[dict, Body]
    ) -> Sensor:
        sensor = Sensor.get_by_name(sensor_name)
        sensor = sensor.set_info(sensor_info=info)
        return sensor

    # Get Platform
    @get("/{sensor_name:str}/platform")
    async def get_sensor_platform(self, sensor_name: str) -> SensorPlatform:
        sensor = Sensor.get_by_name(sensor_name)
        return sensor.sensor_platform

    # Get Data Type
    @get("/{sensor_name:str}/data_type")
    async def get_sensor_data_type(self, sensor_name: str) -> DataType:
        sensor = Sensor.get_by_name(sensor_name)
        return sensor.data_type

    # Get Data Format
    @get("/{sensor_name:str}/data_format")
    async def get_sensor_data_format(self, sensor_name: str) -> DataFormat:
        sensor = Sensor.get_by_name(sensor_name)
        return sensor.data_format

    # Get Sensor Type
    @get("/{sensor_name:str}/sensor_type")
    async def get_sensor_type(self, sensor_name: str) -> SensorType:
        sensor = Sensor.get_by_name(sensor_name)
        return sensor.sensor_type

    # Get Datasets
    @get("/{sensor_name:str}/datasets")
    async def get_sensor_datasets(self, sensor_name: str) -> List[Dataset]:
        sensor = Sensor.get_by_name(sensor_name)
        datasets = sensor.get_datasets()
        return datasets

    # Get Experiments
    @get("/{sensor_name:str}/experiments")
    async def get_sensor_experiments(self, sensor_name: str) -> List[Experiment]:
        sensor = Sensor.get_by_name(sensor_name)
        experiments = sensor.get_experiments()
        return experiments

    # Get Records
    @get("/{sensor_name:str}/records")
    async def get_sensor_records(
        self,
        sensor_name: str,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None,
        plot_number: Optional[int] = None,
        plot_row_number: Optional[int] = None,
        plot_column_number: Optional[int] = None,
    ) -> Stream:
        return Stream(
            sensor_generator(
                sensor_name=sensor_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
            )
        )

    # Add record
    # Create a dataset for sensor and so on
