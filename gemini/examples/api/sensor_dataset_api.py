from gemini.api.sensor import Sensor
from gemini.api.dataset import Dataset, GEMINIDatasetType

# Create a new Sensor for Experiment A
new_sensor = Sensor.create(
    sensor_name="Sensor Test 1",
    sensor_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Sensor: {new_sensor}")

# Create a new Dataset for Experiment A
new_dataset = Dataset.create(
    dataset_name="Dataset Test 1",
    dataset_type=GEMINIDatasetType.Sensor,
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    experiment_name="Experiment A"
)
print(f"Created New Dataset: {new_dataset}")

# Create a new Dataset for New Sensor directly
new_sensor_dataset = new_sensor.create_new_dataset(
    dataset_name="Sensor Test 1 Dataset",
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    experiment_name="Experiment A"
)
print(f"Created New Dataset for New Sensor: {new_sensor_dataset}")

# Associate the new dataset with the new sensor
new_sensor.associate_dataset(dataset_name=new_dataset.dataset_name)
print(f"Associated New Dataset with New Sensor: {new_sensor}")

# Print the associated datasets
associated_datasets = new_sensor.get_associated_datasets()
for dataset in associated_datasets:
    print(f"Associated Dataset: {dataset}")