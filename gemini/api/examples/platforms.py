from gemini.api import SensorPlatform
from gemini.api import Sensor

platform = SensorPlatform.create(sensor_platform_name="Default")

new_sensor = Sensor.create(sensor_name="New Sensor", sensor_info={"type": "camera"})

platform.add_sensor(
    sensor_name=new_sensor.sensor_name,
)

print(platform.sensors)
