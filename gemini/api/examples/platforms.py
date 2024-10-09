from gemini.api import SensorPlatform
from gemini.api import Sensor

platform = SensorPlatform.create(sensor_platform_name="New Platform")
print(f"Created platform: {platform}")

all_platforms = SensorPlatform.all()
print(f"All platforms: {all_platforms}")

new_sensor = Sensor.create(sensor_name="New Sensor", sensor_info={"type": "camera"})
print(f"Created sensor: {new_sensor}")

platform.add_sensor(sensor_name=new_sensor.sensor_name)
print(f"Added sensor to platform: {platform}")

print(f"Platform sensors: {platform.sensors}")
# platform = SensorPlatform.create(sensor_platform_name="Default")

# new_sensor = Sensor.create(sensor_name="New Sensor", sensor_info={"type": "camera"})

# platform.add_sensor(
#     sensor_name=new_sensor.sensor_name,
# )

# print(platform.sensors)
