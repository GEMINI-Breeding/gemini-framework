from gemini.api.sensor_platform import SensorPlatform
from gemini.api.sensor import Sensor, GEMINIDataFormat, GEMINIDataType, GEMINISensorType
from gemini.api.experiment import Experiment

# Create a new sensor platform with experiment Experiment A
new_sensor_platform = SensorPlatform.create(
    sensor_platform_name="Sensor Platform Test 1",
    sensor_platform_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created Sensor Platform: {new_sensor_platform}")

# Assign the sensor platform to Experiment B
new_sensor_platform.assign_experiment("Experiment B")
print(f"Assigned Sensor Platform to Experiment B: {new_sensor_platform}")

# Get all Experiments for the sensor platform
experiments = new_sensor_platform.get_experiments()
print(f"All Experiments:")
for experiment in experiments:
    print(experiment)

# Check if the sensor platform belongs to Experiment B
belongs = new_sensor_platform.belongs_to_experiment("Experiment B")
print(f"Sensor Platform belongs to Experiment B: {belongs}")

# Remove the sensor platform from Experiment B
new_sensor_platform.unassign_experiment("Experiment B")
print(f"Removed Sensor Platform from Experiment B: {new_sensor_platform}")

# Check if it belongs to Experiment B
belongs = new_sensor_platform.belongs_to_experiment("Experiment B")
print(f"Sensor Platform belongs to Experiment B: {belongs}")

# Get Sensor Platform with sensor_platform_name and experiment_name that do exist
sensor_platform = SensorPlatform.get("Sensor Platform Test 1", "Experiment A")
print(f"Got Sensor Platform: {sensor_platform}")

# Get Sensor Platform by ID
sensor_platform = SensorPlatform.get_by_id(new_sensor_platform.id)
print(f"Got Sensor Platform by ID: {sensor_platform}")

# Get all sensor platforms
all_sensor_platforms = SensorPlatform.get_all()
print(f"All Sensor Platforms:")
for sensor_platform in all_sensor_platforms:
    print(sensor_platform)

# Search for sensor platforms
searched_sensor_platforms = SensorPlatform.search(experiment_name="Experiment A")
length_searched_sensor_platforms = len(searched_sensor_platforms)
print(f"Found {length_searched_sensor_platforms} sensor platforms in Experiment A")

# Refresh the sensor platform
sensor_platform.refresh()
print(f"Refreshed Sensor Platform: {sensor_platform}")

# Update the sensor platform
sensor_platform.update(
    sensor_platform_info={"test": "test_updated"},
)
print(f"Updated Sensor Platform: {sensor_platform}")

# Set Sensor Platform Info
sensor_platform.set_info(
    sensor_platform_info={"test": "test_set"},
)
print(f"Set Sensor Platform Info: {sensor_platform}")

# Get Sensor Platform Info
sensor_platform_info = sensor_platform.get_info()
print(f"Sensor Platform Info: {sensor_platform_info}")

# Create a new sensor with experiment Experiment A
new_sensor = sensor_platform.add_sensor(
    sensor_name = "Sensor Test 1",
    sensor_type= GEMINISensorType.Thermal,
    sensor_data_type=GEMINIDataType.Binary,
    sensor_data_format=GEMINIDataFormat.CSV,
    sensor_info={"test": "test"},
    experiment_name="Experiment A",
)
print(f"Created Sensor: {new_sensor}")

# Get all sensors
all_sensors = sensor_platform.get_sensors()
print(f"All Sensors:")
for sensor in all_sensors:
    print(sensor)
