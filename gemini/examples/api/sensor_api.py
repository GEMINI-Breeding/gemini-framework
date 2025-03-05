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

# Create a dataset for the sensor
dataset = sensor.create_dataset(
    dataset_name="Dataset Test 1",
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    experiment_name="Experiment A"
)
print(f"Created Dataset: {dataset}")

# Get all datasets for the sensor
datasets = sensor.get_datasets()
print(f"All Datasets:")
for dataset in datasets:
    print(dataset)

#  Delete the sensor
is_deleted = new_sensor.delete()
print(f"Deleted Sensor: {is_deleted}")




# from gemini.api.sensor import Sensor
# from gemini.api.experiment import Experiment
# from gemini.api.trait import Trait
# from gemini.api.enums import GEMINISensorType, GEMINIDataType, GEMINIDataFormat

# # Create a new sensor with experiment Experiment A
# new_sensor = Sensor.create(
#     sensor_name="Sensor Test 1",
#     sensor_info={"test": "test"},
#     experiment_name="Experiment A"
# )

# # Get Sensor with sensor_name and experiment_name that do exist
# sensor = Sensor.get("Sensor Test 1", "Experiment A")
# print(f"Got Sensor: {sensor}")

# # Get Sensor by ID
# sensor = Sensor.get_by_id(new_sensor.id)
# print(f"Got Sensor by ID: {sensor}")

# # Get all sensors
# all_sensors = Sensor.get_all()
# print(f"All Sensors:")
# for sensor in all_sensors:
#     print(sensor)

# # Search for sensors
# searched_sensors = Sensor.search(experiment_name="Experiment A")
# length_searched_sensors = len(searched_sensors)
# print(f"Found {length_searched_sensors} sensors in Experiment A")

# # Refresh the sensor
# sensor = sensor.refresh()
# print(f"Refreshed Sensor: {sensor}")
