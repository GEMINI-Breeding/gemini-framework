from gemini.api.sensor_type import SensorType

# Create a new Dataset Type
new_sensor_type = SensorType.create(
    sensor_type_name="Test Sensor Type",
    sensor_type_info={
        "description": "This is a test sensor type for API demonstration.",
        "version": "1.0",
    }
)
print(f"Created new sensor type: {new_sensor_type}")

# Get Sensor Type by ID
sensor_type_by_id = SensorType.get_by_id(new_sensor_type.id)
print(f"Sensor Type by ID: {sensor_type_by_id}")

# Get DatasetType by Name
sensor_type_by_name = SensorType.get(sensor_type_name="Test Sensor Type")
print(f"Sensor Type by Name: {sensor_type_by_name}")

# Get all Sensor Types
all_sensor_types = SensorType.get_all()
for sensor_type in all_sensor_types:
    print(sensor_type)

# Search Sensor Types
search_results = SensorType.search(sensor_type_name="Test Sensor Type")
for result in search_results:
    print(f"Search Result: {result}")

# Update Sensor Type
sensor_type = sensor_type.update(
    sensor_type_info={
        "description": "Updated test sensor type for API demonstration.",
        "version": "1.1",
    }
)
print(f"Updated Sensor Type: {sensor_type}")

# Set Sensor Type Info
sensor_type.set_info(
    sensor_type_info={
        "description": "New test sensor type for API demonstration.",
        "version": "2.0",
    }
)
print(f"Sensor Type Info set: {sensor_type.get_info()}")

# Check if Sensor Type exists
sensor_type_exists = SensorType.exists(sensor_type_name="Test Sensor Type")
print(f"Does Sensor Type exist? {sensor_type_exists}")

# Delete Sensor Type
sensor_type.delete()
print(f"Sensor Type deleted: {sensor_type}")

# Check if Sensor Type exists after deletion
sensor_type_exists_after_deletion = SensorType.exists(sensor_type_name="Test Sensor Type")
print(f"Does Sensor Type exist after deletion? {sensor_type_exists_after_deletion}")