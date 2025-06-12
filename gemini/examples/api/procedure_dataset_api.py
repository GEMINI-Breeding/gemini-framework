from gemini.api.procedure import Procedure
from gemini.api.dataset import Dataset, GEMINIDatasetType

# Create a new procedure for Experiment A
new_procedure = Procedure.create(
    procedure_name="Procedure Test 1",
    procedure_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Procedure: {new_procedure}")

# Create a new Dataset for Experiment A
new_dataset = Dataset.create(
    dataset_name="Dataset Test 1",
    dataset_type=GEMINIDatasetType.Procedure,
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    experiment_name="Experiment A"
)
print(f"Created New Dataset: {new_dataset}")

# Create a new Dataset for New Procedure directly
new_procedure_dataset = new_procedure.create_new_dataset(
    dataset_name="Procedure Test 1 Dataset",
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    experiment_name="Experiment A"
)
print(f"Created New Dataset for New Procedure: {new_procedure_dataset}")

# Associate the new dataset with the new procedure
new_procedure.associate_dataset(dataset_name=new_dataset.dataset_name)
print(f"Associated New Dataset with New Procedure: {new_procedure}")

# Print the associated datasets
associated_datasets = new_procedure.get_associated_datasets()
for dataset in associated_datasets:
    print(f"Associated Dataset: {dataset}")