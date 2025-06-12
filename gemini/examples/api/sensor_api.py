from gemini.api.sensor import Sensor
from gemini.api.sensor import GEMINISensorType, GEMINIDataType, GEMINIDataFormat

# Create a new Sensor for Experiment A
new_sensor = Sensor.create(
    sensor_name="Sensor A",
    sensor_type=GEMINISensorType.Calibration,
    sensor_data_format=GEMINIDataFormat.CSV,
    sensor_data_type=GEMINIDataType.Text,
    sensor_info={"test": "test"},
    experiment_name="Experiment A",
    sensor_platform_name="Platform A"
)
print(f"Created New Sensor: {new_sensor}")

# Get Sensor by ID
sensor_by_id = Sensor.get_by_id(new_sensor.id)
print(f"Got Sensor by ID: {sensor_by_id}")

# Get Sensor by Name
sensor_by_name = Sensor.get(sensor_name=new_sensor.sensor_name)
print(f"Got Sensor by Name: {sensor_by_name}")

# Get all Sensors
all_sensors = Sensor.get_all()
for sensor in all_sensors:
    print(f"Sensor: {sensor}")

# Search for Sensors by Name
search_results = Sensor.search(sensor_name="Sensor A")
for result in search_results:
    print(f"Search Result: {result}")

# Update Sensor
sensor_by_name.update(
    sensor_data_format=GEMINIDataFormat.JSON,
    sensor_info={"updated": "info"}
)
print(f"Updated Sensor: {sensor_by_name}")

# Refresh Sensor
sensor_by_name.refresh()
print(f"Refreshed Sensor: {sensor_by_name}")

# Set Sensor Info
sensor_by_name.set_info(
    sensor_info={"new": "info"}
)
print(f"Set Sensor Info: {sensor_by_name.get_info()}")

# Check if Sensor Exists
exists = Sensor.exists(sensor_name="Sensor A")
print(f"Does Sensor Exist? {exists}")

# Delete Sensor
is_deleted = sensor_by_name.delete()
print(f"Deleted Sensor: {is_deleted}")

# Check if Sensor Exists after Deletion
exists_after_deletion = Sensor.exists(sensor_name="Sensor A")
print(f"Does Sensor Exist after Deletion? {exists_after_deletion}")