from gemini.api.cultivar import Cultivar

# Create a new cultivar for Experiment A
new_cultivar = Cultivar.create(
    cultivar_population="Cultivar Test 1",
    cultivar_accession="Accession A",
    cultivar_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created Cultivar: {new_cultivar}")

# Get Associated Experiments
associated_experiments = new_cultivar.get_associated_experiments()
for experiment in associated_experiments:
    print(f"Associated Experiment: {experiment}")

# Associate the cultivar with Experiment B
new_cultivar.associate_experiment(experiment_name="Experiment B")
print(f"Associated Cultivar with Experiment B")

# Check if the cultivar is associated with Experiment B
is_associated = new_cultivar.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Cultivar associated with Experiment B? {is_associated}")

# Unassociate the cultivar from Experiment B
new_cultivar.unassociate_experiment(experiment_name="Experiment B")
print(f"Unassociated Cultivar from Experiment B")

# Verify the unassociation
is_associated_after_unassociation = new_cultivar.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Cultivar still associated with Experiment B? {is_associated_after_unassociation}")