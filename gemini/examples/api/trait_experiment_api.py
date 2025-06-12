from gemini.api.trait import Trait

# Create a new trait for Experiment A
new_trait = Trait.create(
    trait_name="Trait Test 1",
    trait_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Trait: {new_trait}")

# Get associated experiments
associated_experiments = new_trait.get_associated_experiments()
for experiment in associated_experiments:
    print(f"Associated Experiment: {experiment}")

# Associate the trait with Experiment B
new_trait.associate_experiment(experiment_name="Experiment B")
print(f"Associated Trait with Experiment B")

# Check if the trait is associated with Experiment B
is_associated = new_trait.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Trait associated with Experiment B? {is_associated}")

# Unassociate the trait from Experiment B
new_trait.unassociate_experiment(experiment_name="Experiment B")
print(f"Unassociated Trait from Experiment B")

# Verify the unassociation
is_associated_after_unassociation = new_trait.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Trait still associated with Experiment B? {is_associated_after_unassociation}")