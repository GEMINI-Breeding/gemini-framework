from gemini.api.model import Model

# Create a new model
model = Model.create(
    model_name="Model Test 1",
    model_info={"test": "test"},
    model_url="https://example.com/model_test_1",
    experiment_name="Experiment A"
)
print(f"Created Model: {model}")

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

# Get all datasets for the model
model_datasets = model.get_datasets()
print(f"All Model Datasets:")
for model_dataset in model_datasets:
    print(model_dataset)


# Delete the model
is_deleted = model.delete()
print(f"Deleted Model: {is_deleted}")