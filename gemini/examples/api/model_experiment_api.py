from gemini.api.model import Model

# Create a new model for Experiment A
new_model = Model.create(
    model_name="Model Test 1",
    model_url="https://example.com/model_test_1",
    model_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Model: {new_model}")

# Get associated experiments
associated_experiments = new_model.get_associated_experiments()
for experiment in associated_experiments:
    print(f"Associated Experiment: {experiment}")

# Associate the model with Experiment B
new_model.associate_experiment(experiment_name="Experiment B")
print(f"Associated Model with Experiment B")

# Check if the model is associated with Experiment B
is_associated = new_model.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Model associated with Experiment B? {is_associated}")

# Unassociate the model from Experiment B
new_model.unassociate_experiment(experiment_name="Experiment B")
print(f"Unassociated Model from Experiment B")

# Verify the unassociation
is_associated_after_unassociation = new_model.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Model still associated with Experiment B? {is_associated_after_unassociation}")