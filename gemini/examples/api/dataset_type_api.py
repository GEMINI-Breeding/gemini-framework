from gemini.api.dataset_type import DatasetType

# Create a new dataset type
new_dataset_type = DatasetType.create(
    dataset_type_name="Dataset Type Test 1",
    dataset_type_info={"test": "test"},
)

# Get Dataset Type with dataset_type_name that does exist
dataset_type = DatasetType.get("Dataset Type Test 1")
print(f"Got Dataset Type: {dataset_type}")

# Get Dataset Type by ID
dataset_type = DatasetType.get_by_id(new_dataset_type.id)
print(f"Got Dataset Type by ID: {dataset_type}")

# Get all dataset types
all_dataset_types = DatasetType.get_all()
print(f"All Dataset Types:")
for dataset_type in all_dataset_types:
    print(dataset_type)

# Search for dataset types
searched_dataset_types = DatasetType.search(dataset_type_name="Dataset Type Test 1")
length_searched_dataset_types = len(searched_dataset_types)
print(f"Found {length_searched_dataset_types} dataset types")

# Update the dataset type
dataset_type.update(
    dataset_type_info={"test": "test_updated"},
)
print(f"Updated Dataset Type: {dataset_type}")

# Set Dataset Type Info
dataset_type.set_info(
    dataset_type_info={"test": "test_set"},
)
print(f"Set Dataset Type Info: {dataset_type}")

# Get Dataset Type Info
dataset_type_info = dataset_type.get_info()
print(f"Dataset Type Info: {dataset_type_info}")

# Refresh the dataset type
dataset_type.refresh()
print(f"Refreshed Dataset Type: {dataset_type}")

# Delete the new dataset type
is_deleted = new_dataset_type.delete()
print(f"Deleted Dataset Type: {is_deleted}")