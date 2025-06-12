from gemini.api.dataset_type import DatasetType

# Create a new dataset type
new_dataset_type = DatasetType.create(
    dataset_type_name="Test Dataset Type",
    dataset_type_info={
        "description": "This is a test dataset type for API demonstration.",
        "version": "1.0",
    }
)
print(f"Created new dataset type: {new_dataset_type}")

# Get Dataset Type by ID
dataset_type_by_id = DatasetType.get_by_id(new_dataset_type.id)
print(f"Dataset Type by ID: {dataset_type_by_id}")

# Get Dataset Type by Name
dataset_type_by_name = DatasetType.get(dataset_type_name="Test Dataset Type")
print(f"Dataset Type by Name: {dataset_type_by_name}")

# Get all Dataset Types
all_dataset_types = DatasetType.get_all()
for dataset_type in all_dataset_types:
    print(dataset_type)

# Search Dataset Types
search_results = DatasetType.search(dataset_type_name="Test Dataset Type")
for result in search_results:
    print(f"Search Result: {result}")

# Update Dataset Type
dataset_type = dataset_type.update(
    dataset_type_info={
        "description": "Updated test dataset type for API demonstration.",
        "version": "1.1",
    }
)
print(f"Updated Dataset Type: {dataset_type}")

# Set Dataset Type Info
dataset_type.set_info(
    dataset_type_info={
        "description": "New test dataset type for API demonstration.",
        "version": "2.0",
    }
)
print(f"Dataset Type Info set: {dataset_type.get_info()}")

# Check if Dataset Type exists
dataset_type_exists = DatasetType.exists(dataset_type_name="Test Dataset Type")
print(f"Does Dataset Type exist? {dataset_type_exists}")

# Delete Dataset Type
dataset_type.delete()
print(f"Dataset Type deleted: {dataset_type}")

# Check if Dataset Type exists after deletion
dataset_type_exists_after_deletion = DatasetType.exists(dataset_type_name="Test Dataset Type")
print(f"Does Dataset Type exist after deletion? {dataset_type_exists_after_deletion}")