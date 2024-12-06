from gemini.db.models.scripts import ScriptModel

# Get all scripts
scripts = ScriptModel.all()

# Print scripts
print("Scripts:")
for script in scripts:
    print(f"{script.id}: {script.script_name}")
    # Print Runs of Script
    for run in script.script_runs:
        print(f"Run: {run.id}")

    # Print Datasets of Script
    for dataset in script.datasets:
        print(f"Dataset: {dataset.dataset_name}")