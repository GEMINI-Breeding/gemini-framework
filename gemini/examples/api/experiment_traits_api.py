from gemini.api.experiment import Experiment
from gemini.api.trait import Trait

# Create a new trait for Experiment A
new_trait = Trait.create(
    trait_name="New Trait",
    trait_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Trait: {new_trait}")

# Get Experiment B
experiment_b = Experiment.get("Experiment B")
print(f"Got Experiment B: {experiment_b}")

# Associate Experiment B with the new trait
experiment_b.associate_trait(trait_name=new_trait.trait_name)
print(f"Associated New Trait with Experiment B: {experiment_b}")

# Get Associated Traits
associated_traits = experiment_b.get_associated_traits()
for trait in associated_traits:
    print(f"Associated Trait: {trait}")

# Check if the new trait is associated with Experiment B
is_associated = experiment_b.belongs_to_trait(trait_name=new_trait.trait_name)
print(f"Is New Trait associated with Experiment B? {is_associated}")

# Unassociate the new trait from Experiment B
experiment_b.unassociate_trait(trait_name=new_trait.trait_name)
print(f"Unassociated New Trait from Experiment B: {experiment_b}")

# Check if the new trait is still associated with Experiment B
is_associated = experiment_b.belongs_to_trait(trait_name=new_trait.trait_name)
print(f"Is New Trait still associated with Experiment B? {is_associated}")

# Create a new trait for Experiment B
experiment_trait = experiment_b.create_new_trait(
    trait_name="Experiment B Trait",
    trait_info={"test": "test"}
)
print(f"Created New Trait: {experiment_trait}")