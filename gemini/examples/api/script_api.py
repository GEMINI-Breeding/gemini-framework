from gemini.api.script import Script
from gemini.api.experiment import Experiment

# Create a new script with experiment Experiment A
new_script = Script.create(
    script_name="Script Test 1",
    script_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created Script: {new_script}")

# Get Script with script_name and experiment_name that do exist
script = Script.get("Script Test 1", "Experiment A")
print(f"Got Script: {script}")

# Get Script by ID
script = Script.get_by_id(new_script.id)
print(f"Got Script by ID: {script}")

# Get all scripts
all_scripts = Script.get_all()
print(f"All Scripts:")
for script in all_scripts:
    print(script)

# Search for scripts
searched_scripts = Script.search(experiment_name="Experiment A")
length_searched_scripts = len(searched_scripts)
print(f"Found {length_searched_scripts} scripts in Experiment A")

# Refresh the script
script = script.refresh()
print(f"Refreshed Script: {script}")

# Update the script
script.update(
    script_info={"test": "test_updated"},
)
print(f"Updated Script: {script}")

# Create 10 new script runs
for i in range(10):
    script.create_run(
        script_run_info={
            "test_info": f"test_value_{i}"
        }
    )
    print(f"Created Script Run {i + 1}")

# Get all runs for the script
script_runs = script.get_runs()
print(f"All Script Runs:")
for script_run in script_runs:
    print(script_run)

# Create a Dataset for the script
dataset = script.create_dataset(
    dataset_name="Dataset Test 1",
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    experiment_name="Experiment A",
)
print(f"Created Dataset: {dataset}")

# Get all datasets for the script
script_datasets = script.get_datasets()
print(f"All Script Datasets:")
for script_dataset in script_datasets:
    print(script_dataset)

# Delete the script
is_deleted = script.delete()
print(f"Deleted Script: {is_deleted}")
