from gemini.api.trait import Trait
from gemini.api.dataset import Dataset, GEMINIDatasetType

# Create a new trait for Experiment A
new_trait = Trait.create(
    trait_name="Trait Test 1",
    trait_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Trait: {new_trait}")

# Create a new dataset for Experiment A
new_dataset = Dataset.create(
    dataset_name="Dataset Trait Test 1",
    dataset_type=GEMINIDatasetType.Trait,
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    experiment_name="Experiment A"
)
print(f"Created New Dataset: {new_dataset}")

# Create a new Dataset for New Trait directly
new_trait_dataset = new_trait.create_new_dataset(
    dataset_name="Trait Test 1 Dataset",
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    experiment_name="Experiment A"
)
print(f"Created New Dataset for New Trait: {new_trait_dataset}")

# Associate the new dataset with the new trait
new_trait.associate_dataset(dataset_name=new_dataset.dataset_name)
print(f"Associated New Dataset with New Trait: {new_trait}")

# Print the associated datasets
associated_datasets = new_trait.get_associated_datasets()
for dataset in associated_datasets:
    print(f"Associated Dataset: {dataset}")
