from gemini.api.sensor import Sensor
from gemini.api.experiment import Experiment
from gemini.api.trait import Trait
from gemini.api.enums import GEMINISensorType, GEMINIDataType, GEMINIDataFormat

# Create a new sensor with experiment Experiment A
new_sensor = Sensor.create(
    sensor_name="Sensor Test 1",
    sensor_info={"test": "test"},
    experiment_name="Experiment A"
)

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
sensor = sensor.refresh()
print(f"Refreshed Sensor: {sensor}")
