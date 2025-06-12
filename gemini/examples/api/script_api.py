from gemini.api.script import Script

# Create a new script for Experiment A
new_script = Script.create(
    script_name="Script Test 1",
    script_url="https://example.com/script_test_1",
    script_extension="py",
    script_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Script: {new_script}")

# Get Script by ID
script_from_id = Script.get(new_script.id)
print(f"Got Script from ID: {script_from_id}")

# Get Script by Name
script_from_name = Script.get(script_name="Script Test 1")
print(f"Got Script from Name: {script_from_name}")

# Get all scripts
all_scripts = Script.get_all()
for script in all_scripts:
    print(f"Script: {script}")

# Search for scripts by name
search_results = Script.search(script_name="Script Test 1")
for result in search_results:
    print(f"Search Result: {result}")

# Update Script
script_from_name.update(
    script_url="https://example.com/updated_script_test_1",
    script_info={"updated": "info"}
)
print(f"Updated Script: {script_from_name}")

# Refresh Script
script_from_name.refresh()
print(f"Refreshed Script: {script_from_name}")

# Set Script Info
script_from_name.set_info(
    script_info={"new": "info"}
)
print(f"Set Script Info: {script_from_name.get_info()}")

# Check if Script Exists
exists = Script.exists(script_name="Script Test 1")
print(f"Does Script Exist? {exists}")

# Delete Script
is_deleted = script_from_name.delete()
print(f"Deleted Script: {is_deleted}")

# Check if Script Exists after Deletion
exists_after_deletion = Script.exists(script_name="Script Test 1")
print(f"Does Script Exist after Deletion? {exists_after_deletion}")

# Delete Script
is_deleted = new_script.delete()
print(f"Deleted Script: {is_deleted}")

# Check if Script Exists after Deletion
exists_after_deletion = Script.exists(script_name="Script Test 1")
print(f"Does Script Exist after Deletion? {exists_after_deletion}")

