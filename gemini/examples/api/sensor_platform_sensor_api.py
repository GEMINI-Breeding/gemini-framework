from gemini.api.sensor_platform import SensorPlatform
from gemini.api.sensor import Sensor

# Create a new Sensor Platform for Experiment A
new_sensor_platform = SensorPlatform.create(
    sensor_platform_name="Platform Test 1",
    sensor_platform_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Sensor Platform: {new_sensor_platform}")

# Create a new Sensor for Experiment A and Platform Test 1
new_sensor = Sensor.create(
    sensor_name="Sensor Test 1",
    sensor_info={"test": "test"},
    experiment_name="Experiment A",
    sensor_platform_name="Platform Test 1"
)
print(f"Created New Sensor: {new_sensor}")

# Create a new sensor directly
new_sensor_direct = Sensor.create(
    sensor_name="Sensor Test 2",
    sensor_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Sensor Directly: {new_sensor_direct}")

# List Associated Sensor Platforms
associated_sensors = new_sensor_platform.get_associated_sensors()
for sensor in associated_sensors:
    print(f"Associated Sensor: {sensor}")

# Check if the new sensor is associated with Platform Test 1
is_associated = new_sensor_platform.belongs_to_sensor(sensor_name="Sensor Test 1")
print(f"Is Sensor Test 1 associated with Platform Test 1? {is_associated}")

# Unassociate the new sensor from Platform Test 1
new_sensor_platform.unassociate_sensor(sensor_name="Sensor Test 1")
print(f"Unassociated Sensor Test 1 from Platform Test 1")

# Verify the unassociation
is_associated_after_unassociation = new_sensor_platform.belongs_to_sensor(sensor_name="Sensor Test 1")
print(f"Is Sensor Test 1 still associated with Platform Test 1? {is_associated_after_unassociation}")
