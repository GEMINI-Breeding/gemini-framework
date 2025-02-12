from gemini.api.script import Script
from gemini.api.experiment import Experiment

# Create a new script with experiment Experiment A
new_script = Script.create(
    script_name="Script Test 1",
    script_info={"test": "test"},
    experiment_name="Experiment A"
)

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