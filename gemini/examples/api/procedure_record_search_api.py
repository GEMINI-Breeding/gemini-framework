from gemini.api.procedure import Procedure
import os
from datetime import datetime, timedelta

# Create Procedure X
procedure = Procedure.create(
    procedure_name="Procedure X",
    procedure_info={
        "description": "Procedure X for Experiment A"
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

# Add a single record to Procedure X
success, id_list = procedure.add_record(
    timestamp=starting_timestamp,
    collection_date=starting_timestamp.date(),
    procedure_data={
        "data": "test_data"
    },
    experiment_name="Experiment A",
    season_name="Season 1A",
    site_name="Site A1",
    record_info={
        "test_info": "test_value"
    },
    record_file=os.path.join(images_folder, single_image)
)
print(f"Added Record Success: {success}, IDs: {id_list}")

# Add multiple records to Procedure X
timestamps = [starting_timestamp + timedelta(minutes=i+1) for i in range(9)]
procedure_data = [{"data": f"test_data_{i}"} for i in range(9)]
record_files = [os.path.join(images_folder, img) for img in other_images]
record_info = [{"test_info": f"test_value_{i}"} for i in range(9)]
success, id_list = procedure.add_records(
    timestamps=timestamps,
    collection_date=starting_timestamp.date(),
    procedure_data=procedure_data,
    experiment_name="Experiment A",
    season_name="Season 1A",
    site_name="Site A1",
    record_info=record_info,
    record_files=record_files
)
print(f"Added Records Success: {success}, IDs: {id_list}")

# Search for records in Procedure X
procedure_records = procedure.get_records(experiment_name="Experiment A")
procedure_records = [record for record in procedure_records]
print(f"Number of Records: {len(procedure_records)}")