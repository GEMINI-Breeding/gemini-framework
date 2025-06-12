from gemini.api.model import Model

# Get Model A
model_a = Model.get("Model A")
print(f"Got Model A: {model_a}")

# Create a new model run for Model A
new_model_a_run = model_a.create_new_run(
    model_run_info={"test": "test"}
)

# Get Associated Model Runs
associated_model_runs = model_a.get_associated_runs()
for model_run in associated_model_runs:
    print(f"Associated Model Run: {model_run}")

