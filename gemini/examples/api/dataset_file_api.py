from gemini.api.dataset_record import DatasetRecord
from gemini.api.dataset import Dataset
from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site

import os

experiment = Experiment.get(experiment_name="Test Experiment 1")
season = Season.get(season_name="Test Season 1", experiment_name="Test Experiment 1")
site = Site.get(site_name="Test Site 1")

# Get Dataset named Test Dataset
test_dataset = Dataset.get(dataset_name="Test Dataset 1")

# Get Current Script Directory
current_directory = os.path.dirname(os.path.realpath(__file__))

image_folder = os.path.join(current_directory, 'sample_images') 
images = []

for root, dirs, files in os.walk(image_folder):
    for file in files:
        if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
            images.append(os.path.join(root, file))

dataset_records = []
for i, image in enumerate(images):
    record = DatasetRecord(
        timestamp=f"2021-01-01T00:00:00.{i:03d}Z",
        collection_date="2021-01-01",
        dataset_id=test_dataset.id,
        dataset_name=test_dataset.dataset_name,
        dataset_data={},
        experiment_id=experiment.id,
        experiment_name=experiment.experiment_name,
        season_id=season.id,
        season_name=season.season_name,
        site_id=site.id,
        site_name=site.site_name,
        record_file=image,
        record_info={}
    )
    dataset_records.append(record)

test_dataset.add_records(records=dataset_records)


