from gemini.db.models.traits import TraitModel

# Get Default Traits
traits = TraitModel.get_by_parameters(trait_name="Default")
print(f"Trait: {traits.id}: {traits.trait_name}")

# Get Trait Type
trait_level = traits.trait_level
print(f"Trait Level: {trait_level.id}: {trait_level.trait_level_name}")

# Get Trait Datasets
datasets = traits.datasets
print("Datasets:")
for dataset in datasets:
    print(f"Dataset: {dataset.id}: {dataset.dataset_name}")

