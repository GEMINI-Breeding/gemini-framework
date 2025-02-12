from gemini.api.model import Model
from gemini.api.experiment import Experiment

# Create a new model with experiment Experiment A
new_model = Model.create(
    model_name="Model Test 1",
    model_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created Model: {new_model}")

# Get Model with model_name and experiment_name that do exist
model = Model.get("Model Test 1", "Experiment A")

# Get Model by ID
model = Model.get_by_id(new_model.id)

# Get all models
all_models = Model.get_all()
for model in all_models:
    print(model)

# Search for models
searched_models = Model.search(experiment_name="Experiment A")
length_searched_models = len(searched_models)
print(f"Found {length_searched_models} models in Experiment A")

# Refresh the model
model = model.refresh()
print(f"Refreshed Model: {model}")