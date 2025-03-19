from gemini.api.sensor import Sensor
import os
from datetime import datetime, timedelta

# Create Sensor X
sensor = Sensor.create(
    sensor_name="Sensor X",
    sensor_info={
        "description": "Sensor X for Experiment A"
    },
    experiment_name="Experiment A"
)

# Starting timestamp for records
starting_timestamp = datetime.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

# Get Images
script_folder = os.path.dirname(os.path.abspath(__file__))
images_folder = os.path.join(script_folder, "sample_images")
images = os.listdir(images_folder)

# Sort the images by file name
images.sort()
single_image = images[0]
other_images = images[1:]

# Add a single record to Sensor X
success, id_list = sensor.add_record(
    timestamp=starting_timestamp,
    collection_date=starting_timestamp.date(),
    sensor_data={
        "data": "test_data"
    },
    experiment_name="Experiment A",
    season_name="Season 1A",
    site_name="Site A1",
    plot_number=990,
    plot_row_number=991,
    plot_column_number=992,
    record_info={
        "test_info": "test_value"
    },
    record_file=os.path.join(images_folder, single_image)
)
print(f"Added Record Success: {success}, IDs: {id_list}")

# Add multiple records to Sensor X
timestamps = [starting_timestamp + timedelta(minutes=i+1) for i in range(9)]
sensor_data = [{"data": f"test_data_{i}"} for i in range(9)]
record_files = [os.path.join(images_folder, img) for img in other_images]
record_info = [{"test_info": f"test_value_{i}"} for i in range(9)]
plot_numbers = [990 + i for i in range(9)]
plot_row_numbers = [991 + i for i in range(9)]
plot_column_numbers = [992 + i for i in range(9)]

success, id_list = sensor.add_records(
    timestamps=timestamps,
    collection_date=starting_timestamp.date(),
    sensor_data=sensor_data,
    experiment_name="Experiment A",
    season_name="Season 1A",
    site_name="Site A1",
    plot_numbers=plot_numbers,
    plot_row_numbers=plot_row_numbers,
    plot_column_numbers=plot_column_numbers,
    record_info=record_info,
    record_files=record_files
)
print(f"Added Records Success: {success}, IDs: {id_list}")

# Search for the sensor records
sensor_records = sensor.get_records(experiment_name="Experiment A")
sensor_records = [record for record in sensor_records]
print(f"Number of Records Found: {len(sensor_records)}")