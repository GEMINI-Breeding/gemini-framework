from gemini.api import Script
from random import randint
from datetime import datetime, timedelta
import os

start_date = "2021-01-01"
end_date = "2021-01-05"
script_name = "Weather Script"
records_per_day = 144
weather_script = Script.create(
    script_name=script_name,
    experiment_name="GEMINI",
)

current_date = start_date
while current_date <= end_date:

    records_to_add = []

    timestamps = []
    script_data = []

    for i in range(records_per_day):
        timestamp = f"{current_date} {i // 6}:{(i % 6) * 10}:00"
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        timestamps.append(timestamp)

        script_value = randint(0, 40)
        script_data.append({"script_value": script_value, "script_units": "Celsius"})

    weather_script.add_records(
        script_data=script_data,
        timestamps=timestamps,
        dataset_name=f"{script_name}_{current_date}",
        experiment_name="GEMINI",
        season_name="2021",
        site_name="Davis"
    )

    current_date = (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    
    
# Get GEMINI Experiment
from gemini.api import Experiment
experiment = Experiment.get(experiment_name="GEMINI")

# Create new script to test file upload
file_script = Script.create(
    script_name="File Script",
    experiment_name="GEMINI",
)

# Read the files
data_folder = os.path.join(os.path.dirname(__file__), "weather_station_data")
data_files = os.listdir(data_folder)

timestamps = []
script_data = []

for data_file in data_files:
    
    file_path = os.path.join(data_folder, data_file)
    
    timestamp = os.path.getmtime(file_path)
    timestamps.append(datetime.fromtimestamp(timestamp))
    
    script_data.append({
        "file": file_path
    })
    
file_script.add_records(
    script_data=script_data,
    timestamps=timestamps,
    experiment_name="GEMINI",
    season_name="2021",
    site_name="Davis"
)

# Download the files
script_data = file_script.get_records()
for record in script_data:
    print(record.script_data)