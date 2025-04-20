from gemini.api.sensor import Sensor
from gemini.api.enums import GEMINIDataFormat, GEMINIDataType, GEMINISensorType

new_sensor = Sensor.create(
    sensor_name="Sensor Test 1",
    sensor_info={"test": "test"},
    sensor_type=GEMINISensorType.Calibration,
    sensor_data_type=GEMINIDataType.Image,
    sensor_data_format=GEMINIDataFormat.PNG,
    experiment_name="Experiment A",
    sensor_platform_name="Platform A",
)
print(f"Created Sensor: {new_sensor}")

# Assign the sensor to Experiment B
new_sensor.assign_experiment("Experiment B")
print(f"Assigned Sensor to Experiment B: {new_sensor}")

# Get all Experiments for the sensor
experiments = new_sensor.get_experiments()
print(f"All Experiments:")
for experiment in experiments:
    print(experiment)

# Check if the sensor belongs to Experiment B
belongs = new_sensor.belongs_to_experiment("Experiment B")
print(f"Sensor belongs to Experiment B: {belongs}")

# Remove the sensor from Experiment B
new_sensor.unassign_experiment("Experiment B")
print(f"Removed Sensor from Experiment B: {new_sensor}")

# Check if it belongs to Experiment B
belongs = new_sensor.belongs_to_experiment("Experiment B")
print(f"Sensor belongs to Experiment B: {belongs}")

# Get Sensor with sensor_name and experiment_name that do exist
sensor = Sensor.get("Sensor Test 1", "Experiment A")
print(f"Got Sensor: {sensor}")

# Get Sensor by ID
sensor = Sensor.get_by_id(new_sensor.id)
print(f"Got Sensor by ID: {sensor}")

# Get all sensors
all_sensors = Sensor.get_all()
print(f"All Sensors:")
for sensor in all_sensors:
    print(sensor)

# Search for sensors
searched_sensors = Sensor.search(experiment_name="Experiment A")
length_searched_sensors = len(searched_sensors)
print(f"Found {length_searched_sensors} sensors in Experiment A")

# Refresh the sensor
sensor.refresh()
print(f"Refreshed Sensor: {sensor}")

# Update the sensor
sensor.update(
    sensor_info={"test": "test_updated"},
    sensor_type=GEMINISensorType.Default,
    sensor_data_type=GEMINIDataType.Default,
    sensor_data_format=GEMINIDataFormat.Default
)
print(f"Updated Sensor: {sensor}")

# Set Sensor Info
sensor.set_info(
    sensor_info={"test": "test_set"},
)
print(f"Set Sensor Info: {sensor}")

# Get Sensor Info
sensor_info = sensor.get_info()
print(f"Sensor Info: {sensor_info}")

# Create a dataset for the sensor
dataset = sensor.create_dataset(
    dataset_name="Dataset Test 1",
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    experiment_name="Experiment A"
)
print(f"Created Dataset: {dataset}")

# Check sensor has_dataset
has_dataset = sensor.has_dataset("Dataset Test 1")
print(f"Sensor has Dataset Test 1: {has_dataset}")

# Get all datasets for the sensor
datasets = sensor.get_datasets()
print(f"All Datasets:")
for dataset in datasets:
    print(dataset)

#  Delete the sensor
is_deleted = new_sensor.delete()
print(f"Deleted Sensor: {is_deleted}")

