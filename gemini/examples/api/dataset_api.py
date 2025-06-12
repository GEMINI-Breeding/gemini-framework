from gemini.api.dataset import Dataset, GEMINIDatasetType

# Create a new dataset for Experiment A
new_dataset = Dataset.create(
    dataset_name="Test Dataset",
    dataset_type=GEMINIDatasetType.Sensor,
    dataset_info={
        "description": "This is a test dataset for API demonstration.",
        "version": "1.0",
    },
    collection_date="2023-10-01",
    experiment_name="Experiment A"
)
print(f"Created Dataset: {new_dataset}")

# Get Dataset by ID
dataset_by_id = Dataset.get_by_id(new_dataset.id)
print(f"Dataset by ID: {dataset_by_id}")

# Get Dataset by Name
dataset_by_name = Dataset.get(dataset_name="Test Dataset")
print(f"Dataset by Name: {dataset_by_name}")

# Get all Datasets
all_datasets = Dataset.get_all()
for dataset in all_datasets:
    print(dataset)

# Search Datasets
search_results = Dataset.search(experiment_name="Experiment A")
for result in search_results:
    print(f"Search Result: {result}")

# Update Dataset
dataset = dataset.update(
    dataset_info={
        "description": "Updated test dataset for API demonstration.",
        "version": "1.1",
    },
    collection_date="2023-10-02",
)
print(f"Updated Dataset: {dataset}")

# Set Dataset Info
dataset.set_info(
    dataset_info={
        "description": "New test dataset for API demonstration.",
        "version": "2.0",
    }
)
print(f"Dataset Info set: {dataset.get_info()}")

# Check if Dataset exists
dataset_exists = Dataset.exists(dataset_name="Test Dataset")
print(f"Does Dataset exist? {dataset_exists}")

# Delete Dataset
dataset.delete()
print(f"Dataset deleted: {dataset}")

# Check if Dataset exists after deletion
dataset_exists_after_deletion = Dataset.exists(dataset_name="Test Dataset")
print(f"Does Dataset exist after deletion? {dataset_exists_after_deletion}")
