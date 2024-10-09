from gemini.api import Sensor
from gemini.server.database.models import SensorRecordsIMMVModel

sensor = Sensor.get(sensor_name="Campbell CR1000")

sensor_records = sensor.get_records()

for record in sensor_records:
    print(record.sensor_data)