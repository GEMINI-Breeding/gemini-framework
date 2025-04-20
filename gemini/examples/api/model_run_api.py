from gemini.api.model import Model
from gemini.api.model_run import ModelRun

# Get model by name
model = Model.get("Model A")
print(f"Got Model: {model}")

# Create a new model run
model_run = ModelRun.create(
    model_run_info={"test": "test"},
    model_name=model.model_name
)
print(f"Created Model Run: {model_run}")

# Check if created model run exists
exists = ModelRun.exists(
    model_run_info={"test": "test"},
    model_name=model.model_name
)
print(f"Model Run exists: {exists}")

# Check a model run that does not exist
exists = ModelRun.exists(
    model_run_info={"test": "nonexistent"},
    model_name=model.model_name
)
print(f"Nonexistent Model Run exists: {exists}")

# Get ModelRun with model_run_info that does exist
model_run = ModelRun.get({"test": "test"}, model_name=model.model_name)
print(f"Got ModelRun: {model_run}")

# Get ModelRun by ID
model_run = ModelRun.get_by_id(model_run.id)
print(f"Got ModelRun by ID: {model_run}")

# Get all model runs
all_model_runs = ModelRun.get_all()
print(f"All Model Runs:")
for model_run in all_model_runs:
    print(model_run)

# Search for model runs
searched_model_runs = ModelRun.search(model_name=model.model_name)
length_searched_model_runs = len(searched_model_runs)
print(f"Found {length_searched_model_runs} model runs")

# Refresh the model run
model_run.refresh()
print(f"Refreshed Model Run: {model_run}")

# Update the model run
model_run.update(
    model_run_info={"test": "test_updated"},
)
print(f"Updated Model Run: {model_run}")

# Set ModelRun Info
model_run.set_info(
    model_run_info={"test": "test_set"},
)
print(f"Set ModelRun Info: {model_run}")
# Get ModelRun Info
model_run_info = model_run.get_info()
print(f"ModelRun Info: {model_run_info}")

# Delete the model run
is_deleted = model_run.delete()
print(f"Deleted Model Run: {is_deleted}")
