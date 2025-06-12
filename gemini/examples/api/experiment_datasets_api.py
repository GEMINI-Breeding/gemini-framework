from gemini.api.experiment import Experiment
from gemini.api.dataset import Dataset

# Create a new dataset for Experiment A
new_dataset = Dataset.create(
    dataset_name="New Dataset",
    dataset_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Dataset: {new_dataset}")

# Get Experiment B
experiment_b = Experiment.get("Experiment B")
print(f"Got Experiment B: {experiment_b}")

# Associate Experiment B with the new dataset
experiment_b.associate_dataset(dataset_name=new_dataset.dataset_name)
print(f"Associated New Dataset with Experiment B: {experiment_b}")

# Get Associated Datasets
associated_datasets = experiment_b.get_associated_datasets()
for dataset in associated_datasets:
    print(f"Associated Dataset: {dataset}")

# Check if the new dataset is associated with Experiment B
is_associated = experiment_b.belongs_to_dataset(dataset_name=new_dataset.dataset_name)
print(f"Is New Dataset associated with Experiment B? {is_associated}")

# Unassociate the new dataset from Experiment B
experiment_b.unassociate_dataset(dataset_name=new_dataset.dataset_name)
print(f"Unassociated New Dataset from Experiment B: {experiment_b}")

# Check if the new dataset is still associated with Experiment B
is_associated = experiment_b.belongs_to_dataset(dataset_name=new_dataset.dataset_name)
print(f"Is New Dataset still associated with Experiment B? {is_associated}")

# Create a new dataset for Experiment B
experiment_dataset = experiment_b.create_new_dataset(
    dataset_name="Experiment B Dataset",
    dataset_info={"test": "test"}
)
print(f"Created New Dataset: {experiment_dataset}")