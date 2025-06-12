from gemini.api.experiment import Experiment
from gemini.api.model import Model

# Create a new model for Experiment A
new_model = Model.create(
    model_name="New Model",
    model_url="gs://gemini-models/new_model.pkl",
    model_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Model: {new_model}")

# Get Experiment B
experiment_b = Experiment.get("Experiment B")
print(f"Got Experiment B: {experiment_b}")

# Associate Experiment B with the new model
experiment_b.associate_model(model_name=new_model.model_name)
print(f"Associated New Model with Experiment B: {experiment_b}")

# Get Associated Models
associated_models = experiment_b.get_associated_models()
for model in associated_models:
    print(f"Associated Model: {model}")

# Check if the new model is associated with Experiment B
is_associated = experiment_b.belongs_to_model(model_name=new_model.model_name)
print(f"Is New Model associated with Experiment B? {is_associated}")

# Unassociate the new model from Experiment B
experiment_b.unassociate_model(model_name=new_model.model_name)
print(f"Unassociated New Model from Experiment B: {experiment_b}")

# Check if the new model is still associated with Experiment B
is_associated = experiment_b.belongs_to_model(model_name=new_model.model_name)
print(f"Is New Model still associated with Experiment B? {is_associated}")

# Create a new model for Experiment B
experiment_model = experiment_b.create_new_model(
    model_name="Experiment B Model",
    model_url="gs://gemini-models/experiment_b_model.pkl",
    model_info={"test": "test"}
)
print(f"Created New Model: {experiment_model}")