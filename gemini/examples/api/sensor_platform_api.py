from gemini.api.sensor_platform import SensorPlatform
from gemini.api.experiment import Experiment

# Create a new sensor platform with experiment Experiment A
new_sensor_platform = SensorPlatform.create(
    sensor_platform_name="Sensor Platform Test 1",
    sensor_platform_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created Sensor Platform: {new_sensor_platform}")

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