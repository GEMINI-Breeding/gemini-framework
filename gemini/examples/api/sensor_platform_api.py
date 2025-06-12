from gemini.api.sensor_platform import SensorPlatform

# Create a new Sensor Platform for Experiment A
new_sensor_platform = SensorPlatform.create(
    sensor_platform_name="Platform XYZ",
    sensor_platform_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Sensor Platform: {new_sensor_platform}")

# Get Sensor Platform with sensor_platform_name
sensor_platform = SensorPlatform.get(
    sensor_platform_name=new_sensor_platform.sensor_platform_name
)
print(f"Retrieved Sensor Platform: {sensor_platform}")

# Get Sensor Platform with sensor_platform_id
sensor_platform = SensorPlatform.get_by_id(
    id=new_sensor_platform.id
)
print(f"Retrieved Sensor Platform by ID: {sensor_platform}")

# Get all Sensor Platforms
sensor_platforms = SensorPlatform.get_all()
for platform in sensor_platforms:
    print(f"Sensor Platform: {platform}")

# Search for Sensor Platforms
sensor_platforms = SensorPlatform.search(
    sensor_platform_name="Platform XYZ"
)
for platform in sensor_platforms:
    print(f"Search Result: {platform}")

# Refresh Sensor Platform
sensor_platform.refresh()
print(f"Refreshed Sensor Platform: {sensor_platform}")

# Update Sensor Platform
sensor_platform.update(
    sensor_platform_info={"test": "test_updated"}
)
print(f"Updated Sensor Platform: {sensor_platform}")

# Set Sensor Platform Info
sensor_platform.set_info(
    sensor_platform_info={"test": "test_set"}
)
print(f"Set Sensor Platform Info: {sensor_platform.get_info()}")

# Check if Sensor Platform Exists before deletion
exists = SensorPlatform.exists(
    sensor_platform_name="Platform XYZ"
)
print(f"Sensor Platform exists: {exists}")

# Delete Sensor Platform
is_deleted = sensor_platform.delete()
print(f"Deleted Sensor Platform: {is_deleted}")

# Check if Sensor Platform Exists after deletion
exists_after_deletion = SensorPlatform.exists(
    sensor_platform_name="Platform XYZ"
)
print(f"Sensor Platform exists after deletion: {exists_after_deletion}")