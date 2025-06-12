from gemini.api.script import Script
from gemini.api.dataset import Dataset, GEMINIDatasetType

# Create a new script for Experiment A
new_script = Script.create(
    script_name="Script Test 1",
    script_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Script: {new_script}")

# Create a new Dataset for Experiment A
new_dataset = Dataset.create(
    dataset_name="Dataset Test X",
    dataset_type=GEMINIDatasetType.Script,
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    experiment_name="Experiment A"
)
print(f"Created New Dataset: {new_dataset}")

# Create a new Dataset for New Script directly
new_script_dataset = new_script.create_new_dataset(
    dataset_name="Script Test 1 Dataset",
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    experiment_name="Experiment A"
)
print(f"Created New Dataset for New Script: {new_script_dataset}")

# Associate the new dataset with the new script
new_script.associate_dataset(dataset_name=new_dataset.dataset_name)
print(f"Associated New Dataset with New Script: {new_script}")

# Print the associated datasets
associated_datasets = new_script.get_associated_datasets()
for dataset in associated_datasets:
    print(f"Associated Dataset: {dataset}")