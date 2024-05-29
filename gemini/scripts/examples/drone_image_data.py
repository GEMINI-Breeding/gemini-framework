from gemini.api import Sensor, SensorRecord, SensorPlatform
from gemini.api import Experiment
from gemini.api import GEMINIDataFormat, GEMINIDataType, GEMINISensorType

from datetime import datetime
import os

from rich.progress import track

# Get GEMINI Experiment
gemini_experiment = Experiment(experiment_name="GEMINI")

# Create a new platform for Drone
drone_platform = SensorPlatform.create(
    sensor_platform_name="Drone iPhone",
    sensor_platform_info={
        "manufacturer": "Apple",
        "model": "iPhone 12 Pro Max",
        "description": "The iPhone 12 Pro Max is a smartphone designed and marketed by Apple Inc. It is the largest iPhone that Apple has ever produced, with a 6.7-inch display.",
    },
)

# Create a Drone iPhone RGB Camera sensor for the Drone platform
iphone_rgb_sensor = Sensor.create(
    sensor_name="iPhone RGB Camera",
    sensor_type=GEMINISensorType.RGB,
    sensor_data_type=GEMINIDataType.Image,
    sensor_data_format=GEMINIDataFormat.PNG,
    sensor_info={
        "manufacturer": "Apple",
        "model": "iPhone 12 Pro Max",
        "description": "The iPhone 12 Pro Max is a smartphone designed and marketed by Apple Inc. It is the largest iPhone that Apple has ever produced, with a 6.7-inch display.",
    },
    sensor_platform_name="Drone iPhone",
    experiment_name="GEMINI",
)

# Read the files
data_folder = os.path.join(os.path.dirname(__file__), "image_data")
data_files = os.listdir(data_folder)

sensor_records = []

timestamps = []
sensor_data = []

for data_file in data_files:

    file_path = os.path.join(data_folder, data_file)

    timestamp = os.path.getmtime(file_path)
    timestamps.append(datetime.fromtimestamp(timestamp))

    sensor_data.append({
        "file": file_path
    })

iphone_rgb_sensor.add_records(
    timestamps=timestamps,
    sensor_data=sensor_data,
    experiment_name="GEMINI",
    season_name="2023",
    site_name="Davis"
)






    




    