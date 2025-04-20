from gemini.api.dataset import Dataset, GEMINIDatasetType

# Create a new dataset
new_dataset = Dataset.create(
    dataset_name="Dataset Test 1",
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    dataset_type=GEMINIDatasetType.Sensor,
    experiment_name="Experiment A"
)
print(f"Created Dataset: {new_dataset}")

# Check if dataset exists
exists = Dataset.exists(
    dataset_name="Dataset Test 1",
)
print(f"Dataset exists: {exists}")

# Check a dataset that does not exist
exists = Dataset.exists(
    dataset_name="Nonexistent Dataset",
)
print(f"Nonexistent Dataset exists: {exists}")

# Assign the dataset to Experiment B
new_dataset.assign_experiment("Experiment B")
print(f"Assigned Dataset to Experiment B: {new_dataset}")

# Get all Experiments for the dataset
experiments = new_dataset.get_experiments()
print(f"All Experiments:")
for experiment in experiments:
    print(experiment)

# Check if the dataset belongs to Experiment B
belongs = new_dataset.belongs_to_experiment("Experiment B")
print(f"Dataset belongs to Experiment B: {belongs}")

# Remove the dataset from Experiment B
new_dataset.unassign_experiment("Experiment B")
print(f"Removed Dataset from Experiment B: {new_dataset}")

# Get Dataset with dataset_name that does exist
dataset = Dataset.get("Dataset Test 1")
print(f"Got Dataset: {dataset}")

# Get Dataset Type
dataset_type = dataset.get_type()
print(f"Dataset Type: {dataset_type}")

# Get Dataset by ID
dataset = Dataset.get_by_id(new_dataset.id)
print(f"Got Dataset by ID: {dataset}")

# Get all datasets
all_datasets = Dataset.get_all()
print(f"All Datasets:")
for dataset in all_datasets:
    print(dataset)

# Search for datasets
searched_datasets = Dataset.search(experiment_name="Experiment A")
length_searched_datasets = len(searched_datasets)
print(f"Found {length_searched_datasets} datasets in Experiment A")

# Refresh the dataset
dataset.refresh()
print(f"Refreshed Dataset: {dataset}")

# Update the dataset
dataset.update(
    collection_date="2023-10-02",
    dataset_type=GEMINIDatasetType.Trait,
    dataset_info={"test": "test_updated"},

)
print(f"Updated Dataset: {dataset}")

# Set Dataset Info
dataset.set_info(
    dataset_info={"test": "test_set"},
)
print(f"Set Dataset Info: {dataset}")

# Get Dataset Info
dataset_info = dataset.get_info()
print(f"Dataset Info: {dataset_info}")

# Delete the new dataset
is_deleted = new_dataset.delete()
print(f"Deleted Dataset: {is_deleted}")