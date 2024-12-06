from gemini.db.models.sensor_platforms import SensorPlatformModel

# Get all sensor platforms
sensor_platforms = SensorPlatformModel.all()

# Print sensor platforms
for platform in sensor_platforms:
    print(f"{platform.id}: {platform.sensor_platform_name}")
    for sensor in platform.sensors:
        print(f"Sensor: {sensor.sensor_name}")