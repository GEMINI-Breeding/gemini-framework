from gemini.api.sensor_record import SensorRecord
from gemini.api.sensor import Sensor
from gemini.api.plot import Plot
from gemini.api.experiment import Experiment

from datetime import datetime, timedelta
import os

# Create a new sensor for Experiment A
sensor = Sensor.create(
    sensor_name="Test Sensor A",
    sensor_info={
        "test_info": "test_value"
    },
    experiment_name="Experiment A"
)
print(f"Created Sensor: {sensor}")

# Starting timestamp for the records
starting_timestamp = datetime.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
records_to_add = []

# Create a new sensor dataset
dataset = sensor.create_dataset(
    dataset_name="Test Sensor Dataset A",
    collection_date=starting_timestamp.date(),
    experiment_name="Experiment A"
)
print(f"Created Sensor Dataset: {dataset}")

# Get valid combinations for the sensor
valid_combinations = SensorRecord.get_valid_combinations(sensor_name=sensor.sensor_name)
print(f"Valid Combinations: {valid_combinations}")
print(f"Number of Valid Combinations: {len(valid_combinations)}")

# Get Images
script_folder = os.path.dirname(os.path.abspath(__file__))
images_folder = os.path.join(script_folder, "sample_images")
images = os.listdir(images_folder)

# Sort the images by file name
images.sort()
print(images)

for valid_combination in valid_combinations:
    experiment_name = valid_combination['experiment_name']
    site_name = valid_combination['site_name']
    season_name = valid_combination['season_name']
    dataset_name = valid_combination['dataset_name']
    record_info = {
        "test_info": "test_value"
    }
    plot = Plot.get(
        experiment_name=experiment_name,
        site_name=site_name,
        season_name=season_name,
        plot_number=1,
        plot_row_number=1,
        plot_column_number=1,
    )

    for i in range(10):
        timestamp = starting_timestamp + timedelta(minutes=i)
        record_info = {
            "test_info": f"test_value_{i}"
        }
        image_path = os.path.join(images_folder, images[i])
        new_sensor_record = SensorRecord.create(
            experiment_name=experiment_name,
            site_name=site_name,
            season_name=season_name,
            sensor_name=sensor.sensor_name,
            dataset_name=dataset.dataset_name,
            record_info=record_info,
            plot_column_number=plot.plot_column_number,
            plot_row_number=plot.plot_row_number,
            plot_number=plot.plot_number,
            record_file=image_path,
            sensor_data={
                "data": images[i]
            },
            timestamp=timestamp
        )
        records_to_add.append(new_sensor_record)

    starting_timestamp += timedelta(days=1)

# Add the sensor records to the dataset
insert_success = SensorRecord.add(records=records_to_add)
print(f"Insert Success: {insert_success}")

# Outputs
home_dir = os.path.expanduser("~")
output_dir = os.path.join(home_dir, "gemini_sensor_output")
os.makedirs(output_dir, exist_ok=True)

# Get the sensor records
searched_records = SensorRecord.search(
    sensor_name=sensor.sensor_name,
    collection_date="2021-01-01",
)
searched_records = [record for record in searched_records]
print(f"Found {len(searched_records)} sensor records")

# Save the sensor records to the output directory
for record in searched_records:
    downloaded_file_path = record.get_record_file(download_folder=output_dir)
    print(f"Downloaded file path: {downloaded_file_path}")
        
