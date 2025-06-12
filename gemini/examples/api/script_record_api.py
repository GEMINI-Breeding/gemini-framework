from gemini.api.script import ScriptRecord
from datetime import datetime, timedelta
from random import randint

timestamp = datetime(1994, 10, 1, 12, 0, 0)  # Fixed timestamp for consistency
timestamp = timestamp + timedelta(hours=randint(0, 23), minutes=randint(0, 59))  # Randomize time within the day

# Create a new Script Record for Script A, with Experiment A, Site A1 and Season 1A
new_script_record = ScriptRecord.create(
    timestamp=timestamp,
    collection_date=timestamp.date(),
    script_name="Script A",
    dataset_name="Script A Dataset",
    script_data={"key": "value"},
    experiment_name="Experiment A",
    site_name="Site A1",
    season_name="Season 1A",
    record_info={"test": "test"},
    insert_on_create=True
)
print(f"Created Script Record: {new_script_record}")

# Get Script Record by ID
script_record_by_id = ScriptRecord.get_by_id(new_script_record.id)
print(f"Script Record by ID: {script_record_by_id}")

# Get Script Record
script_record_by_name = ScriptRecord.get(
    timestamp=new_script_record.timestamp,
    script_name="Script A",
    dataset_name="Script A Dataset",
    experiment_name="Experiment A",
    site_name="Site A1",
    season_name="Season 1A"
)
print(f"Script Record by Name: {script_record_by_name}")

# Get all Script Records limit by 10
script_records = ScriptRecord.get_all(limit=10)
print(f"Script Records (limit 10):")
for record in script_records:
    print(record)

# Search Script Records
searched_records = ScriptRecord.search(
    experiment_name="Experiment A"
)
searched_records = list(searched_records)  # Convert to list to evaluate the generator
print(f"Found {len(searched_records)} records in Experiment A:")

# Update the newly created Script Record
updated_record = new_script_record.update(
    script_data={"key": "new_value"},
    record_info={"test": "test_updated"}
)
print(f"Updated Script Record: {updated_record}")

# Set Script Record Info
updated_record.set_info(
    record_info={"test": "test_set_info"}
)
print(f"Script Record Info set: {updated_record.get_info()}")

# Check if Script Record exists
exists = ScriptRecord.exists(
    timestamp=new_script_record.timestamp,
    script_name="Script A",
    dataset_name="Script A Dataset",
    experiment_name="Experiment A",
    site_name="Site A1",
    season_name="Season 1A"
)
print(f"Does Script Record Exist? {exists}")

# Delete Script Record
is_deleted = updated_record.delete()
print(f"Deleted Script Record: {is_deleted}")

# Check if Script Record exists after deletion
exists_after_deletion = ScriptRecord.exists(
    timestamp=new_script_record.timestamp,
    script_name="Script A",
    dataset_name="Script A Dataset",
    experiment_name="Experiment A",
    site_name="Site A1",
    season_name="Season 1A"
)
print(f"Does Script Record Exist after Deletion? {exists_after_deletion}")

