from gemini.db.models.sensors import SensorModel

# Get Default Sensor
sensor = SensorModel.get_by_parameters(sensor_name="Default")
print(f"Sensor: {sensor.id}: {sensor.sensor_name}")

# Get Sensor Type
sensor_type = sensor.sensor_type
print(f"Sensor Type: {sensor_type.id}: {sensor_type.sensor_type_name}")

# Get Sensor Data Type
sensor_data_type = sensor.sensor_data_type
print(f"Sensor Data Type: {sensor_data_type.id}: {sensor_data_type.data_type_name}")

# Get Sensor Format
sensor_format = sensor.sensor_data_format
print(f"Sensor Format: {sensor_format.id}: {sensor_format.data_format_name}")  

# Get Datasets
datasets = sensor.datasets
print("Datasets:")
for dataset in datasets:
    print(f"Dataset: {dataset.id}: {dataset.dataset_name}")