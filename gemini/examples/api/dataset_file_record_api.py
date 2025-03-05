from gemini.api.dataset_record import DatasetRecord
from gemini.api.dataset import Dataset
from gemini.api.plot import Plot
from gemini.api.experiment import Experiment

from datetime import datetime, timedelta
import os

# Create a new dataset for Experiment A
dataset = Dataset.create(
    dataset_name="Test Dataset A",
    dataset_info={
        "test_info": "test_value"
    },
    experiment_name="Experiment A"
)

# Starting timestamp for the records
starting_timestamp = datetime.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
records_to_add = []

# Create a new dataset collection

# Get valid combinations for the dataset
valid_combinations = DatasetRecord.get_valid_combinations(dataset_name=dataset.dataset_name)
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
    record_info = {
        "test_info": "test_value"
    }
    for i in range(10):
        timestamp = starting_timestamp + timedelta(minutes=i)
        record_info = {
            "test_info": f"test_value_{i}"
        }
        image_path = os.path.join(images_folder, images[i])
        new_dataset_record = DatasetRecord.create(
            dataset_name=dataset.dataset_name,
            experiment_name=experiment_name,
            site_name=site_name,
            season_name=season_name,
            record_info=record_info,
            record_file=image_path,
            dataset_data={
                "data": image_path
            },
            collection_date=starting_timestamp.date(),
            timestamp=timestamp
        )
        print(f"Created Dataset Record: {new_dataset_record}")
        records_to_add.append(new_dataset_record)

    starting_timestamp += timedelta(days=1)

# Add the dataset records to the database
insert_success = DatasetRecord.add(records=records_to_add)
print(f"Insert Success: {insert_success}")

# Outputs
home_dir = os.path.expanduser("~")
output_folder = os.path.join(home_dir, "gemini_dataset_records")
os.makedirs(output_folder, exist_ok=True)

# Search for the dataset records in the collection
searched_records = DatasetRecord.search(
    dataset_name=dataset.dataset_name,
    collection_date="2021-01-01",
)
searched_records = [record for record in searched_records]
print(f"Found {len(searched_records)} records in the collection.")

for record in searched_records:
    downloaded_file_path = record.get_record_file(download_folder=output_folder)
    print(f"Downloaded file: {downloaded_file_path}")
