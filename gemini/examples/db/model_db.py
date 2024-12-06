from gemini.db.models.models import ModelModel

# Get Default Model
default_model = ModelModel.get_by_parameters(model_name='Default')

# Print Default Model Runs
print("Default Model Runs:")
for model_run in default_model.model_runs:
    print(f"{model_run.id}: {model_run.model_run_info}")

# Print Default Model Datasets
print("Default Model Datasets:")
for dataset in default_model.datasets:
    print(f"{dataset.id}: {dataset.dataset_name}")