from gemini.api import Procedure
from random import randint
from datetime import datetime, timedelta
import os

start_date = "2021-01-01"
end_date = "2021-01-05"
procedure_name = "Plant Watering"
records_per_day = 144
plant_watering_procedure = Procedure.create(
    procedure_name=procedure_name,
    experiment_name="GEMINI",
)

current_date = start_date
while current_date <= end_date:

    records_to_add = []

    timestamps = []
    procedure_data = []

    for i in range(records_per_day):
        timestamp = f"{current_date} {i // 6}:{(i % 6) * 10}:00"
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        timestamps.append(timestamp)

        procedure_value = randint(0, 40)
        procedure_data.append({"procedure_value": procedure_value, "procedure_units": "Celsius"})

    plant_watering_procedure.add_records(
        procedure_data=procedure_data,
        timestamps=timestamps,
        dataset_name=f"{procedure_name}_{current_date}",
        experiment_name="GEMINI",
        season_name="2021",
        site_name="Davis",
        plot_numbers=[1] * records_per_day,
    )

    current_date = (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    

# Get GEMINI Experiment
from gemini.api import Experiment
experiment = Experiment.get(experiment_name="GEMINI")

# Create new procedure to test file upload
file_procedure = Procedure.create(
    procedure_name="File Procedure",
    experiment_name="GEMINI",
)

# Read the files
data_folder = os.path.join(os.path.dirname(__file__), "weather_station_data")
data_files = os.listdir(data_folder)

timestamps = []
procedure_data = []

for data_file in data_files:
    
    file_path = os.path.join(data_folder, data_file)
    
    timestamp = os.path.getmtime(file_path)
    timestamps.append(datetime.fromtimestamp(timestamp))
    
    procedure_data.append({
        "file": file_path
    })
    
file_procedure.add_records(
    procedure_data=procedure_data,
    timestamps=timestamps,
    experiment_name="GEMINI",
    season_name="2023",
    site_name="Davis"
)

# Download the procedure data
procedure_data = file_procedure.get_records(experiment_name="GEMINI")
for record in procedure_data:
    print(record.procedure_data)
