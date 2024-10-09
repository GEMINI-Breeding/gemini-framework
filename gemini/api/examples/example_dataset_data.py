from gemini.api import Dataset
from random import randint
from datetime import datetime, timedelta
import os

start_date = "2021-01-01"
end_date = "2021-01-05"
dataset_name = "Plant Evolution"
records_per_day = 144
plant_evolution_dataset = Dataset.create(
    dataset_name=dataset_name,
    experiment_name="GEMINI",
)

current_date = start_date
while current_date <= end_date:

    records_to_add = []

    timestamps = []
    dataset_data = []

    for i in range(records_per_day):
        timestamp = f"{current_date} {i // 6}:{(i % 6) * 10}:00"
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        timestamps.append(timestamp)

        dataset_value = randint(0, 40)
        dataset_data.append({"trait_value": dataset_value, "trait_units": "Celsius"})

    plant_evolution_dataset.add_records(
        dataset_data=dataset_data,
        timestamps=timestamps,
        dataset_name=f"{dataset_name}_{current_date}",
        experiment_name="GEMINI",
        season_name="2021",
        site_name="Davis",
        plot_numbers=[1] * records_per_day,
    )

    current_date = (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    
    
# Get GEMINI Experiment
from gemini.api import Experiment
experiment = Experiment.get(experiment_name="GEMINI")

# Create new dataset to test file upload
file_dataset = Dataset.create(
    dataset_name="File Dataset",
    experiment_name="GEMINI",
)

# Read the files
data_folder = os.path.join(os.path.dirname(__file__), "weather_station_data")
data_files = os.listdir(data_folder)

# dataset_records = []
timestamps = []
dataset_data = []

for data_file in data_files:
    
    file_path = os.path.join(data_folder, data_file)
    
    timestamp = os.path.getmtime(file_path)
    timestamps.append(datetime.fromtimestamp(timestamp))
    
    dataset_data.append({
        "file": file_path
    })
    
file_dataset.add_records(
    timestamps=timestamps,
    dataset_data=dataset_data,
    experiment_name="GEMINI",
    season_name="2023",
    site_name="Davis"
)

# Download dataset data
downloaded_records = file_dataset.get_records()
for record in downloaded_records:
    print(record.dataset_data)