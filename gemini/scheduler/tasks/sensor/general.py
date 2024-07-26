from gemini.api import Sensor, SensorRecord
from gemini.api import Experiment

from datetime import datetime
from prefect import task

@task
def add_sensor_records(
    sensor_name: str,
    sensor_data: list[dict],
    timestamps: list[datetime],
    **kwargs
) -> list[SensorRecord]:
    
    sensor = Sensor(sensor_name=sensor_name)
    added_records = sensor.add_records(
        timestamps=timestamps,
        sensor_data=sensor_data,
        **kwargs
    )
    
    return added_records