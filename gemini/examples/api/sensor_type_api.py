from gemini.api.sensor_type import SensorType

# Create a new sensor type
new_sensor_type = SensorType.create(
    sensor_type_name="Sensor Type Test 1",
    sensor_type_info={"test": "test"},
)

# Get Sensor Type with sensor_type_name that does exist
sensor_type = SensorType.get("Sensor Type Test 1")
print(f"Got Sensor Type: {sensor_type}")

# Get Sensor Type by ID
sensor_type = SensorType.get_by_id(new_sensor_type.id)
print(f"Got Sensor Type by ID: {sensor_type}")

# Get all sensor types
all_sensor_types = SensorType.get_all()
print(f"All Sensor Types:")
for sensor_type in all_sensor_types:
    print(sensor_type)

# Search for sensor types
searched_sensor_types = SensorType.search(sensor_type_name="Sensor Type Test 1")
length_searched_sensor_types = len(searched_sensor_types)
print(f"Found {length_searched_sensor_types} sensor types")

# Update the sensor type
sensor_type.update(
    sensor_type_info={"test": "test_updated"},
)
print(f"Updated Sensor Type: {sensor_type}")

# Set Sensor Type Info
sensor_type.set_info(
    sensor_type_info={"test": "test_set"},
)
print(f"Set Sensor Type Info: {sensor_type}")

# Get Sensor Type Info
sensor_type_info = sensor_type.get_info()
print(f"Sensor Type Info: {sensor_type_info}")

# Refresh the sensor type
sensor_type.refresh()
print(f"Refreshed Sensor Type: {sensor_type}")

# Delete the new sensor type
is_deleted = new_sensor_type.delete()
print(f"Deleted Sensor Type: {is_deleted}")
