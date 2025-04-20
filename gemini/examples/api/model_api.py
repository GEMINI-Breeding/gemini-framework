from gemini.api.model import Model

# Create a new model
model = Model.create(
    model_name="Model Test 1",
    model_info={"test": "test"},
    model_url="https://example.com/model_test_1",
    experiment_name="Experiment A"
)
print(f"Created Model: {model}")

# Check if created model exists
exists = Model.exists(model_name="Model Test 1")
print(f"Model exists: {exists}")

# Check a model that does not exist
exists = Model.exists(model_name="Nonexistent Model")
print(f"Nonexistent Model exists: {exists}")
    

# Assign the model to Experiment B
model.assign_experiment("Experiment B")
print(f"Assigned Model to Experiment B: {model}")

# Get all Experiments for the model
experiments = model.get_experiments()
print(f"All Experiments:")
for experiment in experiments:
    print(experiment)

# Check if the model belongs to Experiment B
belongs = model.belongs_to_experiment("Experiment B")
print(f"Model belongs to Experiment B: {belongs}")

# Remove the model from Experiment B
model.unassign_experiment("Experiment B")
print(f"Removed Model from Experiment B: {model}")

# Check if it belongs to Experiment B
belongs = model.belongs_to_experiment("Experiment B")
print(f"Model belongs to Experiment B: {belongs}")


# Get Model with model_name that does exist
model = Model.get("Model Test 1")
print(f"Got Model: {model}")

# Get Model by ID
model = Model.get_by_id(model.id)
print(f"Got Model by ID: {model}")

# Get all models
all_models = Model.get_all()
print(f"All Models:")
for model in all_models:
    print(model)

# Search for models
searched_models = Model.search(experiment_name="Experiment A")
length_searched_models = len(searched_models)
print(f"Found {length_searched_models} models in Experiment A")

# Refresh the model
model.refresh()
print(f"Refreshed Model: {model}")

# Update the model
model.update(
    model_info={"test": "test_updated"},
)
print(f"Updated Model: {model}")

# Set Model Info
model.set_info(
    model_info={"test": "test_set"},
)
print(f"Set Model Info: {model}")

# Get Model Info
model_info = model.get_info()
print(f"Model Info: {model_info}")

# Create 10 new model runs
for i in range(10):
    model.create_run(
        model_run_info={
            "test_info": f"test_value_{i}"
        }
    )
    print(f"Created Model Run {i + 1}")

# Get all runs for the model
model_runs = model.get_runs()
print(f"All Model Runs:")
for model_run in model_runs:
    print(model_run)

# Create a Dataset for the model
dataset = model.create_dataset(
    dataset_name="Dataset Test 1",
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    experiment_name="Experiment A"
)
print(f"Created Dataset: {dataset}")

# Check if has_dataset for the model
has_dataset = model.has_dataset("Dataset Test 1")
print(f"Model has Dataset Test 1: {has_dataset}")

# Get all datasets for the model
model_datasets = model.get_datasets()
print(f"All Model Datasets:")
for model_dataset in model_datasets:
    print(model_dataset)


# Delete the model
is_deleted = model.delete()
print(f"Deleted Model: {is_deleted}")