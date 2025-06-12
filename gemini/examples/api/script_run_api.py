from gemini.api.script import Script
from gemini.api.script_run import ScriptRun

# Get script by name
script = Script.get("Script A")
print(f"Got Script: {script}")

# Create a new script run
script_run = ScriptRun.create(
    script_run_info={"test": "test"},
    script_name=script.script_name
)
print(f"Created Script Run: {script_run}")

# Get ScriptRun with script_run_info that does exist
script_run = ScriptRun.get({"test": "test"}, script_name=script.script_name)
print(f"Got ScriptRun: {script_run}")

# Get ScriptRun by ID
script_run = ScriptRun.get_by_id(script_run.id)
print(f"Got ScriptRun by ID: {script_run}")

# Get all script runs
all_script_runs = ScriptRun.get_all()
print(f"All Script Runs:")
for script_run in all_script_runs:
    print(script_run)

# Search for script runs
searched_script_runs = ScriptRun.search(script_name=script.script_name)
length_searched_script_runs = len(searched_script_runs)
print(f"Found {length_searched_script_runs} script runs")

# Refresh the script run
script_run.refresh()
print(f"Refreshed Script Run: {script_run}")

# Update the script run
script_run.update(
    script_run_info={"test": "test_updated"},
)
print(f"Updated Script Run: {script_run}")

# Set ScriptRun Info
script_run.set_info(
    script_run_info={"test": "test_set"},
)
print(f"Set ScriptRun Info: {script_run}")

# Get ScriptRun Info
script_run_info = script_run.get_info()
print(f"ScriptRun Info: {script_run_info}")

# Check if ScriptRun exists before deletion
exists = ScriptRun.exists(script_run_info={"test": "test_set"}, script_name=script.script_name)
print(f"ScriptRun exists before deletion: {exists}")

# Delete the script run
is_deleted = script_run.delete()
print(f"Deleted Script Run: {is_deleted}")

# Check if ScriptRun exists after deletion
exists_after_deletion = ScriptRun.exists(script_run_info={"test": "test_set"}, script_name=script.script_name)
print(f"ScriptRun exists after deletion: {exists_after_deletion}")