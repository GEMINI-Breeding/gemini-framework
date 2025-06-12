from gemini.api.script import Script
from gemini.api.script_run import ScriptRun

# Create a new script run for Script A
new_script_run = ScriptRun.create(
    script_run_info={"test": "test"},
    script_name="Script A"
)
print(f"Created New Script Run: {new_script_run}")

# Create a new script for Experiment A
new_script = Script.create(
    script_name="Script  X",
    script_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Script: {new_script}")

# Get associated script of the new script run
associated_script = new_script_run.get_associated_script()
print(f"Associated Script: {associated_script}")

# Associate the new script run with the new script
new_script_run.associate_script(script_name=new_script.script_name)
print(f"Associated New Script Run with New Script: {new_script_run}")

# Check if the new script run is associated with the new script
is_associated = new_script_run.belongs_to_script(script_name=new_script.script_name)
print(f"Is New Script Run associated with New Script? {is_associated}")

# Unassociate the new script run from the new script
new_script_run.unassociate_script()
print(f"Unassociated New Script Run from New Script: {new_script_run}")

# Check if the new script run is still associated with the new script
is_associated = new_script_run.belongs_to_script(script_name=new_script.script_name)
print(f"Is New Script Run still associated with New Script? {is_associated}")