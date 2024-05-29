from gemini.api import Sensor

drone_sensor = Sensor(sensor_name="iPhone RGB Camera")

sensor_records = drone_sensor.get_records()

for record in sensor_records:
    print(record)