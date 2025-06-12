from gemini.api.script import Script

# Create a new script for Experiment A
new_script = Script.create(
    script_name="Script Test 1",
    script_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Script: {new_script}")

# Get associated experiments
associated_experiments = new_script.get_associated_experiments()
for experiment in associated_experiments:
    print(f"Associated Experiment: {experiment}")

# Associate the script with Experiment B
new_script.associate_experiment(experiment_name="Experiment B")
print(f"Associated Script with Experiment B")

# Check if the script is associated with Experiment B
is_associated = new_script.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Script associated with Experiment B? {is_associated}")

# Unassociate the script from Experiment B
new_script.unassociate_experiment(experiment_name="Experiment B")
print(f"Unassociated Script from Experiment B")

# Verify the unassociation
is_associated_after_unassociation = new_script.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Script still associated with Experiment B? {is_associated_after_unassociation}")