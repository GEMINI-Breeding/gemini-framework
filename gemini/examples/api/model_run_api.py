from gemini.api.model_run import ModelRun
from gemini.api.model import Model

# Create a new model run for Model A
new_model_run = ModelRun.create(
    model_run_info={"test": "test"},
    model_name="Model A"
)
print(f"Created New Model Run: {new_model_run}")

# Get Model Run by ID
model_run_b = ModelRun.get(new_model_run.id)
print(f"Got Model Run B: {model_run_b}")

# Get Model Run by Model Name and Model Info
model_run_b = ModelRun.get(
    model_name="Model A",
    model_run_info={"test": "test"}
)
print(f"Got Model Run B: {model_run_b}")

# Get all model runs
all_model_runs = ModelRun.get_all()
print(f"All Model Runs: {all_model_runs}")

# Search for model runs by name
search_results = ModelRun.search(model_name="Model A")
for result in search_results:
    print(f"Search Result: {result}")

# Update Model Run
model_run_b.update(model_run_info={"updated": "info"})
print(f"Updated Model Run B: {model_run_b}")

# Set Model Run Info
model_run_b.set_info(
    model_run_info={"new": "info"}
)
print(f"Set Model Run Info: {model_run_b.get_info()}")

# Refresh Model Run
model_run_b.refresh()
print(f"Refreshed Model Run B: {model_run_b}")

# Check if Model Run Exists
exists = ModelRun.exists(
    model_name="Model A",
    model_run_info={"new": "info"}
)
print(f"Does Model Run Exist? {exists}")

# Delete Model Run
is_deleted = model_run_b.delete()
print(f"Deleted Model Run B: {is_deleted}")

# Check if Model Run Exists after Deletion
exists = ModelRun.exists(
    model_name="Model A",
    model_run_info={"new": "info"}
)
print(f"Does Model Run Exist after Deletion? {exists}")

