from gemini.api.model import Model
from gemini.api.dataset import Dataset, GEMINIDatasetType

# Create a new model for Experiment A
new_model = Model.create(
    model_name="Model Test 1",
    model_url="https://example.com/model_test_1",
    model_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Model: {new_model}")

# Create a new Dataset for Experiment A
new_dataset = Dataset.create(
    dataset_name="Dataset Test 1",
    dataset_type=GEMINIDatasetType.Model,
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    experiment_name="Experiment A"
)
print(f"Created New Dataset: {new_dataset}")

# Create a new Dataset for New Model directly
new_model_dataset = new_model.create_new_dataset(
    dataset_name="Model Test 1 Dataset",
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    experiment_name="Experiment A"
)
print(f"Created New Dataset for New Model: {new_model_dataset}")

# Associate the new dataset with the new model
new_model.associate_dataset(dataset_name=new_dataset.dataset_name)
print(f"Associated New Dataset with New Model: {new_model}")

# Print the associated datasets
associated_datasets = new_model.get_associated_datasets()
for dataset in associated_datasets:
    print(f"Associated Dataset: {dataset}")

