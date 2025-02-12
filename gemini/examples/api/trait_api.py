from gemini.api.trait import Trait, GEMINITraitLevel
from gemini.api.experiment import Experiment

# Create a new trait with experiment Experiment A
new_trait = Trait.create(
    trait_name="Trait Test 1",
    trait_info={"test": "test"},
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
searched_traits = Trait.search(experiment_name="Experiment A")
length_searched_traits = len(searched_traits)
print(f"Found {length_searched_traits} traits in Experiment A")
