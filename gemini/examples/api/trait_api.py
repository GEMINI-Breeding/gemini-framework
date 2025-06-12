from gemini.api.trait import Trait, GEMINITraitLevel


# Create a new trait
new_trait = Trait.create(
    trait_name="Trait Test 1",
    trait_level=GEMINITraitLevel.Plant,
    trait_metrics={"test": "test"},
    trait_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Trait: {new_trait}")

# Get Trait by ID
trait_by_id = Trait.get_by_id(id=new_trait.id)
print(f"Trait by ID: {trait_by_id}")

# Get Trait by Name
trait_by_name = Trait.get(trait_name=new_trait.trait_name)
print(f"Trait by Name: {trait_by_name}")

# Get all Traits
all_traits = Trait.get_all()
for trait in all_traits:
    print(f"All Traits: {trait}")

# Search for Traits
searched_traits = Trait.search(trait_name="Trait Test 1")
for trait in searched_traits:
    print(f"Searched Trait: {trait}")

# Update the trait
trait_by_name.update(
    trait_level=GEMINITraitLevel.Plot,
    trait_metrics={"test": "test_updated"},
    trait_info={"test": "test_updated"},
)
print(f"Updated Trait: {trait_by_name}")

# Set Trait Info
trait_by_name.set_info(
    trait_info={"test": "test_set"},
)
print(f"Set Trait Info: {trait_by_name.get_info()}")

# Refresh Trait
trait_by_name.refresh()
print(f"Refreshed Trait: {trait_by_name}")

# Check if Trait Exists
exists = Trait.exists(trait_name="Trait Test 1")
print(f"Trait exists: {exists}")

# Delete the created trait
is_deleted = trait_by_name.delete()
print(f"Deleted Trait: {is_deleted}")

# Check if Trait Exists after deletion
exists_after_deletion = Trait.exists(trait_name="Trait Test 1")
print(f"Trait exists after deletion: {exists_after_deletion}")