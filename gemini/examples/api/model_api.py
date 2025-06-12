from gemini.api.model import Model

# Create a new model for Experiment A
new_model = Model.create(
    model_name="Model A",
    model_url="https://example.com/model_a",
    model_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Model: {new_model}")

# Get Model by ID
model_from_id = Model.get(new_model.id)
print(f"Got Model from ID: {model_from_id}")

# Get Model by Name
model_from_name = Model.get(model_name="Model A")
print(f"Got Model from Name: {model_from_name}")

# Get all models
all_models = Model.get_all()
for model in all_models:
    print(f"Model: {model}")

# Search for models by name
search_results = Model.search(model_name="Model A")
for result in search_results:
    print(f"Search Result: {result}")

# Update Model
model_from_name.update(
    model_url="https://example.com/updated_model_a",
    model_info={"updated": "info"}
)
print(f"Updated Model: {model_from_name}")

# Refresh Model
model_from_name.refresh()
print(f"Refreshed Model: {model_from_name}")

# Set Model Info
model_from_name.set_info(
    model_info={"new": "info"}
)
print(f"Set Model Info: {model_from_name.get_info()}")

# Check if Model Exists
exists = Model.exists(model_name="Model A")
print(f"Does Model Exist? {exists}")

# Delete Model
is_deleted = model_from_name.delete()
print(f"Deleted Model: {is_deleted}")

# Check if Model Exists after Deletion
exists = Model.exists(model_name="Model A")
print(f"Does Model Exist after Deletion? {exists}")