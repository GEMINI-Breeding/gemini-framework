from gemini.api.dataset import Dataset, GEMINIDatasetType

# Create a new dataset for Experiment A
new_dataset = Dataset.create(
    dataset_name="Test Dataset",
    dataset_type=GEMINIDatasetType.Sensor,
    dataset_info={
        "description": "This is a test dataset for API demonstration.",
        "version": "1.0",
    },
    experiment_name="Experiment A",
    collection_date="2023-10-01"
)
print(f"Created Dataset: {new_dataset}")

# Get associated experiments for the dataset
associated_experiments = new_dataset.get_associated_experiments()
for experiment in associated_experiments:
    print(f"Associated Experiment: {experiment}")

# Associate the dataset with Experiment B
new_dataset.associate_experiment(experiment_name="Experiment B")
print(f"Associated dataset {new_dataset.dataset_name} with Experiment B")

# Check if the dataset is associated with Experiment B
is_associated = new_dataset.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is dataset {new_dataset.dataset_name} associated with Experiment B? {is_associated}")

# Unassociate the dataset from Experiment B
new_dataset.unassociate_experiment(experiment_name="Experiment B")
print(f"Unassociated dataset {new_dataset.dataset_name} from Experiment B")

# Verify the unassociation
is_associated_after_unassociation = new_dataset.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is dataset {new_dataset.dataset_name} still associated with Experiment B? {is_associated_after_unassociation}")