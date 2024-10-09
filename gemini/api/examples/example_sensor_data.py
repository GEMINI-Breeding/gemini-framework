from gemini.api import Sensor
from gemini.api import GEMINISensorType, GEMINIDataType, GEMINIDataFormat
from random import randint
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

start_date = "2021-01-01"
end_date = "2025-01-01"
sensor_name = "Weather Sensor"
records_per_day = 1440
weather_sensor = Sensor.create(
    sensor_name=sensor_name,
    sensor_info={
        "manufacturer": "Gemini",
        "model": "GEMINI-WEATHER-SENSOR",
        "description": "Weather sensor for the GEMINI project"
    },
    experiment_name="GEMINI",
    sensor_platform_name="GEMINI-PLATFORM-01",
    sensor_data_format=GEMINIDataFormat.Default,
    sensor_type=GEMINISensorType.Weather
)

# For everyday between start_date and end_date
current_date = start_date
while current_date <= end_date:

    records_to_add = []

    timestamps = []
    sensor_values = []

    year = int(current_date[:4])

    # 1440 timestamps for that day
    for i in range(records_per_day):
        timestamp = f"{current_date} {i // 60}:{i % 60}:00"
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        timestamps.append(timestamp)

        # Random temperature between 0 and 40
        sensor_value = {
            "temperature": randint(0, 40),
            "humidity": randint(0, 100),
            "pressure": randint(900, 1100),
            "wind_speed": randint(0, 20),
            "wind_direction": randint(0, 360),
            "precipitation": randint(0, 10),
            "solar_radiation": randint(0, 1000),
            "uv_index": randint(0, 10),
            "dew_point": randint(0, 40),
            "cloud_cover": randint(0, 100)
        }

        sensor_values.append(sensor_value)

    weather_sensor.add_records(
        sensor_data=sensor_values,
        timestamps=timestamps,
        dataset_name=f"{sensor_name}_{current_date}",
        experiment_name="GEMINI",
        season_name=year,
        site_name="Davis"
    )



    # Go to next season
    current_date = datetime.strptime(current_date, "%Y-%m-%d") + relativedelta(years=1)
    current_date = current_date.strftime("%Y-%m-%d")