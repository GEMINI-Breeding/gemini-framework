from gemini.api.trait import Trait, GEMINITraitLevel, GEMINIDatasetType

# Create a new trait for experiment Experiment A
new_trait = Trait.create(
    trait_name="Trait Test 1",
    trait_units="units",
    trait_level=GEMINITraitLevel.Plot,
    trait_info={"test": "test", "test2": "test2"},
    trait_metrics={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created Trait: {new_trait}")

# Get Trait with trait_name and experiment_name that do exist
trait = Trait.get("Trait Test 1", "Experiment A")
print(f"Got Trait: {trait}")

# Get Trait by ID
trait = Trait.get_by_id(new_trait.id)
print(f"Got Trait by ID: {trait}")

# Get all traits
all_traits = Trait.get_all()
print(f"All Traits:")
for trait in all_traits:
    print(trait)

# Search for traits
searched_traits = Trait.search(trait_info={"test": "test"})
length_searched_traits = len(searched_traits)
print(f"Found {length_searched_traits} traits in Experiment A")

# Refresh the trait
trait.refresh()
print(f"Refreshed Trait: {trait}")

# Update the trait
trait.update(
    trait_info={"test": "test_updated"},
    trait_units="units_updated",
    trait_level=GEMINITraitLevel.Plant,
    trait_metrics={"test": "test_updated"},
)
print(f"Updated Trait: {trait}")

# Create a dataset for the trait
dataset = trait.create_dataset(
    dataset_name="Dataset Test 1",
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    experiment_name="Experiment A"
)
print(f"Created Dataset: {dataset}")

# Get all datasets for the trait
datasets = trait.get_datasets()
print(f"All Datasets:")
for dataset in datasets:
    print(dataset)

# Delete the trait
is_deleted = new_trait.delete()
print(f"Deleted Trait: {is_deleted}")

