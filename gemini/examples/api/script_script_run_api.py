from gemini.api.script import Script

# Get Script A
script_a = Script.get("Script A")
print(f"Got Script A: {script_a}")

# Create a new script run for Script A
new_script_a_run = script_a.create_new_run(
    script_run_info={"test": "test"}
)
print(f"Created New Script Run: {new_script_a_run}")

# Get Associated Script Runs
associated_script_runs = script_a.get_associated_runs()
for script_run in associated_script_runs:
    print(f"Associated Script Run: {script_run}")