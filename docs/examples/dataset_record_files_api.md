# Dataset Record Files API Example

This example demonstrates how to use the DatasetRecord API to associate files with dataset records in the Gemini framework.

## Source File Location

The original Python script is located at `gemini/examples/api/dataset_record_files_api.py`.

## Code

```python
from gemini.api.dataset_record import DatasetRecord
from datetime import datetime, timedelta
from random import randint
import os

# Create Timestamp
timestamp = datetime(1994, 10, 1, 12, 0, 0)  # Fixed timestamp for consistency
timestamp = timestamp + timedelta(hours=randint(0, 23), minutes=randint(0, 59))  # Randomize time within the day

# Get Sample Image Folder
script_folder = os.path.dirname(os.path.abspath(__file__))
sample_image_folder = os.path.join(script_folder, "sample_images")
sample_image_files = [
    os.path.join(sample_image_folder, f) for f in os.listdir(sample_image_folder)
    if os.path.isfile(os.path.join(sample_image_folder, f))
]
print(f"Sample Image Files: {sample_image_files}")


# Creating Records to add to DatasetRecord
records_to_add = []
for image_file in sample_image_files:
    timestamp = timestamp + timedelta(minutes=randint(1, 60))  # Increment timestamp for each file
    collection_date = timestamp.date()  # Use the date part of the timestamp
    record = DatasetRecord.create(
        timestamp=timestamp,
        collection_date=collection_date,
        dataset_name="Dataset A",
        experiment_name="Experiment A",
        site_name="Site A1",
        season_name="Season 1A",
        record_file=image_file,
        record_info={"test": "test"},
        insert_on_create=False
    )
    records_to_add.append(record)

DatasetRecord.insert(records_to_add)

# Search the Dataset Records
searched_records = DatasetRecord.search(
    collection_date=timestamp.date(),
    dataset_name="Dataset A",
    experiment_name="Experiment A",
    site_name="Site A1",
    season_name="Season 1A"
)
searched_records = list(searched_records)  # Convert to list to evaluate the generator
# Print the searched records
print(f"Found {len(searched_records)} records in Dataset A, Experiment A, Site A1, Season 1A:")
for record in searched_records:
    print(record)

# Insert the file records into the DatasetRecord
# for record in records
```

## Explanation

This example demonstrates how to associate files with dataset records using the Gemini API:

*   **Creating dataset records with files:** The `DatasetRecord.create()` method is used to create new dataset records, each associated with a file from the `sample_images` directory. The `insert_on_create` parameter is set to `False` to allow batch insertion.
*   **Inserting dataset records:** The `DatasetRecord.insert()` method is used to efficiently insert multiple dataset records into the database.
*   **Searching for dataset records:** The `DatasetRecord.search()` method is used to find dataset records based on specified criteria.
