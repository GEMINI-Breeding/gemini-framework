from gemini.api.model_run import ModelRun
from gemini.api.model import Model

# Create a new model run for Model A
new_model_run = ModelRun.create(
    model_run_info={"test": "test"},
    model_name="Model A"
)
print(f"Created New Model Run: {new_model_run}")

# Create a new model for Experiment A
new_model = Model.create(
    model_name="Model  X",
    model_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Model: {new_model}")

# Get associated model of the new model run
associated_model = new_model_run.get_associated_model()
print(f"Associated Model: {associated_model}")

# Associate the new model run with the new model
new_model_run.associate_model(model_name=new_model.model_name)
print(f"Associated New Model Run with New Model: {new_model_run}")

# Check if the new model run is associated with the new model
is_associated = new_model_run.belongs_to_model(model_name=new_model.model_name)
print(f"Is New Model Run associated with New Model? {is_associated}")

# Unassociate the new model run from the new model
new_model_run.unassociate_model()
print(f"Unassociated New Model Run from New Model: {new_model_run}")

# Check if the new model run is still associated with the new model
is_associated = new_model_run.belongs_to_model(model_name=new_model.model_name)
print(f"Is New Model Run still associated with New Model? {is_associated}")