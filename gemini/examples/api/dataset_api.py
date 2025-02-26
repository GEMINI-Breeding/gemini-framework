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

# Get Dataset with dataset_name that does exist
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

# Delete the new dataset
is_deleted = new_dataset.delete()
print(f"Deleted Dataset: {is_deleted}")