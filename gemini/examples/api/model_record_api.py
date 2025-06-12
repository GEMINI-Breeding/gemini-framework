from gemini.api.model_record import ModelRecord
from datetime import datetime, timedelta
from random import randint

timestamp = datetime(1994, 10, 1, 12, 0, 0)  # Fixed timestamp for consistency
timestamp = timestamp + timedelta(hours=randint(0, 23), minutes=randint(0, 59))  # Randomize time within the day

# Create a new Model Record for Model A, Model Dataset A, with Experiment A, Site A1 and Season 1A
new_model_record = ModelRecord.create(
    timestamp=timestamp,
    collection_date=timestamp.date(),
    model_name="Model A",
    dataset_name="Model A Dataset",
    model_data={"key": "value"},
    experiment_name="Experiment A",
    site_name="Site A1",
    season_name="Season 1A",
    record_info={"test": "test"},
    insert_on_create=True
)
print(f"Created Model Record: {new_model_record}")

# Get Model Record by ID
model_record_by_id = ModelRecord.get_by_id(new_model_record.id)
print(f"Model Record by ID: {model_record_by_id}")

# Get Model Record
model_record_by_name = ModelRecord.get(
    timestamp=new_model_record.timestamp,
    model_name="Model A",
    dataset_name="Model A Dataset",
    experiment_name="Experiment A",
    site_name="Site A1",
    season_name="Season 1A"
)
print(f"Model Record by Name: {model_record_by_name}")

# Get all Model Records limit by 10
model_records = ModelRecord.get_all(limit=10)
print(f"Model Records (limit 10):")
for record in model_records:
    print(record)

# Search Model Records
searched_records = ModelRecord.search(
    experiment_name="Experiment A"
)
searched_records = list(searched_records)  # Convert to list to evaluate the generator
print(f"Found {len(searched_records)} records in Experiment A:")

# Update the newly created Model Record
updated_record = new_model_record.update(
    model_data={"key": "new_value"},
    record_info={"test": "test_updated"}
)
print(f"Updated Model Record: {updated_record}")

# Set Model Record Info
updated_record.set_info(
    record_info={"test": "test_set_info"}
)
print(f"Model Record Info set: {updated_record.get_info()}")

# Check if Model Record exists
exists = ModelRecord.exists(
    timestamp=new_model_record.timestamp,
    model_name="Model A",
    dataset_name="Model A Dataset",
    experiment_name="Experiment A",
    site_name="Site A1",
    season_name="Season 1A"
)
print(f"Does Model Record exist? {exists}")

# Delete Model Record
deleted_record = new_model_record.delete()
print(f"Model Record deleted: {deleted_record}")

# Check if Model Record exists after deletion
exists_after_deletion = ModelRecord.exists(
    timestamp=new_model_record.timestamp,
    model_name="Model A",
    dataset_name="Model A Dataset",
    experiment_name="Experiment A",
    site_name="Site A1",
    season_name="Season 1A"
)
print(f"Does Model Record exist after deletion? {exists_after_deletion}")
