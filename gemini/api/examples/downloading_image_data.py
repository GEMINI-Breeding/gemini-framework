from gemini.api import Sensor

drone_sensor = Sensor(sensor_name="iPhone RGB Camera")

print(drone_sensor.get_platform())

sensor_records = drone_sensor.get_records()

for record in sensor_records:
    print(record)