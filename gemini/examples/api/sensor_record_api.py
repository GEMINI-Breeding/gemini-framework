from gemini.api.sensor_record import SensorRecord
from datetime import datetime, timedelta
from random import randint

timestamp = datetime(1994, 10, 1, 12, 0, 0)  # Fixed timestamp for consistency
timestamp = timestamp + timedelta(hours=randint(0, 23), minutes=randint(0, 59))  # Randomize time within the day

# Create a new Sensor Record for Sensor A, with Experiment A, Site A1 and Season 1A
new_sensor_record = SensorRecord.create(
    timestamp=timestamp,
    collection_date=timestamp.date(),
    sensor_name="Sensor A1",
    dataset_name="Sensor A1 Dataset",
    sensor_data={"key": "value"},
    experiment_name="Experiment A",
    site_name="Site A1",
    season_name="Season 1A",
    record_info={"test": "test"},
    plot_number=1,
    plot_row_number=1,
    plot_column_number=1,
    insert_on_create=True
)
print(f"Created Sensor Record: {new_sensor_record}")

# Get Sensor Record by ID
sensor_record_by_id = SensorRecord.get_by_id(new_sensor_record.id)
print(f"Sensor Record by ID: {sensor_record_by_id}")

# Get Sensor Record
sensor_record_by_name = SensorRecord.get(
    timestamp=new_sensor_record.timestamp,
    sensor_name="Sensor A1",
    dataset_name="Sensor A1 Dataset",
    experiment_name="Experiment A",
    site_name="Site A1",
    season_name="Season 1A",
    plot_number=1,
    plot_row_number=1,
    plot_column_number=1
)
print(f"Sensor Record by Name: {sensor_record_by_name}")

# Get all Sensor Records limit by 10
sensor_records = SensorRecord.get_all(limit=10)
print(f"Sensor Records (limit 10):")
for record in sensor_records:
    print(record)

# Search Sensor Records
searched_records = SensorRecord.search(
    experiment_name="Experiment A"
)
searched_records = list(searched_records)  # Convert to list to evaluate the generator
print(f"Found {len(searched_records)} records in Experiment A:")

# Update the newly created Sensor Record
updated_record = new_sensor_record.update(
    sensor_data={"key": "new_value"},
    record_info={"test": "test_updated"}
)
print(f"Updated Sensor Record: {updated_record}")

# Set Sensor Record Info
updated_record.set_info(
    record_info={"test": "test_set_info"}
)
print(f"Set Sensor Record Info: {updated_record.get_info()}")

# Check if Sensor Record Exists
exists = SensorRecord.exists(
    timestamp=new_sensor_record.timestamp,
    sensor_name="Sensor A1",
    dataset_name="Sensor A1 Dataset",
    experiment_name="Experiment A",
    site_name="Site A1",
    season_name="Season 1A",
    plot_number=1,
    plot_row_number=1,
    plot_column_number=1
)
print(f"Does Sensor Record Exist? {exists}")

# Delete Sensor Record
is_deleted = new_sensor_record.delete()
print(f"Deleted Sensor Record: {is_deleted}")

# Check if Sensor Record Exists after Deletion
exists_after_deletion = SensorRecord.exists(
    timestamp=new_sensor_record.timestamp,
    sensor_name="Sensor A1",
    dataset_name="Sensor A1 Dataset",
    experiment_name="Experiment A",
    site_name="Site A1",
    season_name="Season 1A",
    plot_number=1,
    plot_row_number=1,
    plot_column_number=1
)
print(f"Does Sensor Record Exist after Deletion? {exists_after_deletion}")