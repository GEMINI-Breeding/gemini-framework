from gemini.api.trait_level import TraitLevel

# Create a new trait level
new_trait_level = TraitLevel.create(
    trait_level_name="Trait Level Test 1",
    trait_level_info={"test": "test"},
)
print(f"Created Trait Level: {new_trait_level}")

# Get TraitLevel with trait_level_name that does exist
trait_level = TraitLevel.get("Trait Level Test 1")
print(f"Got Trait Level: {trait_level}")

# Get TraitLevel by ID
trait_level = TraitLevel.get_by_id(new_trait_level.id)
print(f"Got Trait Level by ID: {trait_level}")

# Get all trait levels
all_trait_levels = TraitLevel.get_all()
print(f"All Trait Levels:")
for trait_level in all_trait_levels:
    print(trait_level)

# Search for trait levels
searched_trait_levels = TraitLevel.search(trait_level_name="Trait Level Test 1")
length_searched_trait_levels = len(searched_trait_levels)
print(f"Found {length_searched_trait_levels} trait levels")

# Refresh the trait level
trait_level.refresh()
print(f"Refreshed Trait Level: {trait_level}")

# Update the trait level
trait_level.update(
    trait_level_info={"test": "test_updated"},
)
print(f"Updated Trait Level: {trait_level}")

# Set Trait Level Info
trait_level.set_info(
    trait_level_info={"test": "test_set"},
)
print(f"Set Trait Level Info: {trait_level}")

# Get Trait Level Info
trait_level_info = trait_level.get_info()
print(f"Trait Level Info: {trait_level_info}")

# Delete the trait level
is_deleted = new_trait_level.delete()
print(f"Deleted Trait Level: {is_deleted}")