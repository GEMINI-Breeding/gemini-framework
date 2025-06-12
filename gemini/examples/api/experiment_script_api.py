from gemini.api.experiment import Experiment
from gemini.api.script import Script

# Create a new script for Experiment A
new_script = Script.create(
    script_name="New Script",
    script_url="gs://gemini-scripts/new_script.py",
    script_extension="py",
    script_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Script: {new_script}")

# Get Experiment B
experiment_b = Experiment.get("Experiment B")
print(f"Got Experiment B: {experiment_b}")

# Associate Experiment B with the new script
experiment_b.associate_script(script_name=new_script.script_name)
print(f"Associated New Script with Experiment B: {experiment_b}")

# Get Associated Scripts
associated_scripts = experiment_b.get_associated_scripts()
for script in associated_scripts:
    print(f"Associated Script: {script}")

# Check if the new script is associated with Experiment B
is_associated = experiment_b.belongs_to_script(script_name=new_script.script_name)
print(f"Is New Script associated with Experiment B? {is_associated}")

# Unassociate the new script from Experiment B
experiment_b.unassociate_script(script_name=new_script.script_name)
print(f"Unassociated New Script from Experiment B: {experiment_b}")

# Check if the new script is still associated with Experiment B
is_associated = experiment_b.belongs_to_script(script_name=new_script.script_name)
print(f"Is New Script still associated with Experiment B? {is_associated}")

# Create a new script for Experiment B
experiment_script = experiment_b.create_new_script(
    script_name="Experiment B Script",
    script_url="gs://gemini-scripts/experiment_b_script.py",
    script_extension="py",
    script_info={"test": "test"}
)
print(f"Created New Script: {experiment_script}")
