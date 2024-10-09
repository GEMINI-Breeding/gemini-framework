from gemini.api import Sensor, SensorRecord
from gemini.api import Experiment
from gemini.api import GEMINIDataFormat, GEMINIDataType, GEMINISensorType

from datetime import datetime
import os

from rich.progress import track

# Get GEMINI Experiment
gemini_experiment = Experiment(experiment_name="GEMINI")


# Create a new sensor, which is the weather sensor
weather_sensor = Sensor.create(
    sensor_name="Campbell CR1000",
    sensor_type=GEMINISensorType.Weather,
    sensor_data_type=GEMINIDataType.Default,
    sensor_data_format=GEMINIDataFormat.Default,
    sensor_info={
        "manufacturer": "Campbell Scientific",
        "model": "CR1000",
        "description": "The CR1000 is our most widely used data logger. It can be used in a broad range of measurement and control functions. Rugged enough for extreme conditions and reliable enough for remote environments, it is also robust enough for complex configurations. Used in applications all over the world, it will be a powerful core component for your data-acquisition system.",
    },
    experiment_name="GEMINI",
)

# After creating the sensor, lets get the reference to this sensor
weather_sensor = Sensor(sensor_name="Campbell CR1000")

# Read the files
data_folder = os.path.join(os.path.dirname(__file__), "weather_station_data")
data_files = os.listdir(data_folder)

sensor_records = []

for data_file in data_files:

    print(f"Processing file: {data_file}")

    file_path = os.path.join(data_folder, data_file)
    with open(file_path, "r") as f:
        lines = f.readlines()

        column_names = lines[1].strip().split(",")
        column_names = [column_name.strip('"') for column_name in column_names]

        units = lines[2].strip().split(",")
        units = [unit.strip('"') for unit in units]

        timestamps = []
        records_to_add = []

        for line in lines[4:]:
            data = line.strip().split(",")
            data = [value.strip('"') for value in data]

            timestamp = datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S")
            timestamps.append(timestamp)

            collection_date = timestamp.date()
            year = timestamp.year
            record_data = dict(zip(column_names[2:], data[2:]))

            records_to_add.append(record_data)

        print("Number of records to add: ", len(records_to_add))

        added_records = weather_sensor.add_records(
            timestamps=timestamps,
            sensor_data=records_to_add,
            experiment_name="GEMINI",
            season_name=f"{year}",
            site_name="Davis"
        )

        added_records = list(added_records)
        sensor_records.extend(added_records)




        

        



