from gemini.api.dataset import Dataset
from gemini.api.dataset import GEMINIDatasetType
from gemini.api.experiment import Experiment

# Create a new dataset with experiment Experiment A
new_dataset = Dataset.create(
    collection_date="2021-01-01",
    dataset_name="Dataset Test 1",
    dataset_info={"test": "test"},
    dataset_type=GEMINIDatasetType.Script,
    experiment_name="Experiment A"
)
print(f"Created Dataset: {new_dataset}")

# Get Dataset with dataset_name and experiment_name that do exist
dataset = Dataset.get("Dataset Test 1")
print(f"Got Dataset: {dataset}")

# Get Dataset by ID
dataset = Dataset.get_by_id(new_dataset.id)
print(f"Got Dataset by ID: {dataset}")

# Get all datasets
all_datasets = Dataset.get_all()
print(f"All Datasets:")
for dataset in all_datasets:
    print(dataset)

# Search for datasets
searched_datasets = Dataset.search(experiment_name="Experiment Z")
length_searched_datasets = len(searched_datasets)
print(f"Found {length_searched_datasets} datasets in Experiment Z")

# Refresh the dataset
dataset = dataset.refresh()
print(f"Refreshed Dataset: {dataset}")