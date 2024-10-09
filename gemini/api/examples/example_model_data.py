from gemini.api import Model
from random import randint
from datetime import datetime, timedelta
import os

start_date = "2021-01-01"
end_date = "2021-01-05"
model_name = "Weather Model"
records_per_day = 2048
weather_model = Model.create(
    model_name=model_name,
    experiment_name="GEMINI",
)

current_date = start_date
while current_date <= end_date:

    records_to_add = []

    timestamps = []
    model_data = []

    for i in range(records_per_day):
        timestamp = f"{current_date} {i // 6 % 24}:{(i % 6) * 10}:00"
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        timestamps.append(timestamp)

        model_value = randint(0, 40)
        model_data.append({"model_value": model_value, "model_units": "Celsius"})

    weather_model.add_records(
        model_data=model_data,
        timestamps=timestamps,
        dataset_name=f"{model_name}_{current_date}",
        experiment_name="GEMINI",
        season_name="2021",
        site_name="Davis"
    )

    current_date = (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    
# Get GEMINI Experiment
from gemini.api import Experiment
experiment = Experiment.get(experiment_name="GEMINI")

# Create new model to test file upload
file_model = Model.create(
    model_name="File Model",
    experiment_name="GEMINI",
)

# Read the files
data_folder = os.path.join(os.path.dirname(__file__), "weather_station_data")
data_files = os.listdir(data_folder)

timestamps = []
model_data = []

for data_file in data_files:
    
    file_path = os.path.join(data_folder, data_file)
    
    timestamp = os.path.getmtime(file_path)
    timestamps.append(datetime.fromtimestamp(timestamp))
    
    model_data.append({
        "file": file_path
    })
    
file_model.add_records(
    timestamps=timestamps,
    model_data=model_data,
    experiment_name="GEMINI",
    season_name="2021",
    site_name="Davis"
)

# Download the model data
model_data = file_model.get_records(experiment_name="GEMINI")
for record in model_data:
    print(record.model_data)
