from gemini.api.experiment import Experiment
from gemini.api.sensor_platform import SensorPlatform

# Create a new sensor platform for Experiment A
new_sensor_platform = SensorPlatform.create(
    sensor_platform_name="New Sensor Platform",
    sensor_platform_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Sensor Platform: {new_sensor_platform}")

# Get Experiment B
experiment_b = Experiment.get("Experiment B")
print(f"Got Experiment B: {experiment_b}")

# Associate Experiment B with the new sensor platform
experiment_b.associate_sensor_platform(sensor_platform_name=new_sensor_platform.sensor_platform_name)
print(f"Associated New Sensor Platform with Experiment B: {experiment_b}")

# Get Associated Sensor Platforms
associated_sensor_platforms = experiment_b.get_associated_sensor_platforms()
for sensor_platform in associated_sensor_platforms:
    print(f"Associated Sensor Platform: {sensor_platform}")

# Check if the new sensor platform is associated with Experiment B
is_associated = experiment_b.belongs_to_sensor_platform(sensor_platform_name=new_sensor_platform.sensor_platform_name)
print(f"Is New Sensor Platform associated with Experiment B? {is_associated}")

# Unassociate the new sensor platform from Experiment B
experiment_b.unassociate_sensor_platform(sensor_platform_name=new_sensor_platform.sensor_platform_name)
print(f"Unassociated New Sensor Platform from Experiment B: {experiment_b}")

# Check if the new sensor platform is still associated with Experiment B
is_associated = experiment_b.belongs_to_sensor_platform(sensor_platform_name=new_sensor_platform.sensor_platform_name)
print(f"Is New Sensor Platform still associated with Experiment B? {is_associated}")

# Create a new sensor platform for Experiment B
experiment_sensor_platform = experiment_b.create_new_sensor_platform(
    sensor_platform_name="Experiment B Sensor Platform",
    sensor_platform_info={"test": "test"}
)
print(f"Created New Sensor Platform: {experiment_sensor_platform}")