from gemini.api.sensor import Sensor
from gemini.api.sensor_platform import SensorPlatform

# Create a new Sensor Platform for Experiment A
new_sensor_platform = SensorPlatform.create(
    sensor_platform_name="Platform A",
    sensor_platform_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Sensor Platform: {new_sensor_platform}")

# Create a new Sensor for Experiment A
new_sensor = Sensor.create(
    sensor_name="Sensor A",
    sensor_info={"test": "test"},
    experiment_name="Experiment A",
    sensor_platform_name="Platform A"
)
print(f"Created New Sensor: {new_sensor}")

# Get Associated Sensor Platforms
associated_sensor_platforms = new_sensor.get_associated_sensor_platforms()
for sensor_platform in associated_sensor_platforms:
    print(f"Associated Sensor Platform: {sensor_platform}")

# Associate the new sensor with a different Sensor Platform
new_sensor.associate_sensor_platform(sensor_platform_name="Platform B")
print(f"Associated Sensor with Platform B")

# Check if the new sensor is associated with Platform B
is_associated = new_sensor.belongs_to_sensor_platform(sensor_platform_name="Platform B")
print(f"Is Sensor associated with Platform B? {is_associated}")

# Unassociate the new sensor from Platform B
new_sensor.unassociate_sensor_platform(sensor_platform_name="Platform B")
print(f"Unassociated Sensor from Platform B")

# Verify the unassociation
is_associated_after_unassociation = new_sensor.belongs_to_sensor_platform(sensor_platform_name="Platform B")
print(f"Is Sensor still associated with Platform B? {is_associated_after_unassociation}")

