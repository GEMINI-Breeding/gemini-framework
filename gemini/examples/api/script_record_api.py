from gemini.api.script_record import ScriptRecord
from gemini.api.script import Script
from gemini.api.experiment import Experiment
from datetime import datetime, timedelta

# Create a new script for Experiment A
script = Script.create(
    script_name="Test Script A",
    script_info={
        "test_info": "test_value"
    },
    experiment_name="Experiment A"
)
print(f"Created Script: {script}")

# Starting timestamp for the records
starting_timestamp = datetime.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
records_to_add = []

# Create a new script dataset
dataset = script.create_dataset(
    dataset_name="Test Script Dataset A",
    collection_date=starting_timestamp.date(),
    experiment_name="Experiment A"
)
print(f"Created Script Dataset: {dataset}")

# Get valid combinations for the script
valid_combinations = ScriptRecord.get_valid_combinations(script_name=script.script_name)
print(f"Valid Combinations: {valid_combinations}")
print(f"Number of Valid Combinations: {len(valid_combinations)}")

# For each valid combination, add records
for valid_combination in valid_combinations:
    experiment_name = valid_combination['experiment_name']
    site_name = valid_combination['site_name']
    season_name = valid_combination['season_name']
    dataset_name = valid_combination['dataset_name']
    record_info = {
        "test_info": "test_value"
    }
    for i in range(10):
        timestamp = starting_timestamp + timedelta(minutes=i)
        record_info = {
            "test_info": f"test_value_{i}"
        }
        new_script_record = ScriptRecord.create(
            experiment_name=experiment_name,
            site_name=site_name,
            season_name=season_name,
            script_name=script.script_name,
            dataset_name=dataset.dataset_name,
            record_info=record_info,
            script_data={
                "data": "data_" + str(i)
            },
            timestamp=timestamp
        )
        print(f"Created Script Record: {new_script_record}")
        # Add the script record
        records_to_add.append(new_script_record)
    # Increase the starting timestamp for the next combination
    starting_timestamp += timedelta(days=1)

insert_success = ScriptRecord.add(records=records_to_add)
print(f"Insert Success: {insert_success}")

# Search for the script records
one_combination = valid_combinations[0]
search_results = ScriptRecord.search(
    experiment_name=one_combination['experiment_name'],
    site_name=one_combination['site_name'],
    season_name=one_combination['season_name'],
    script_name=script.script_name,
    dataset_name=one_combination['dataset_name']
)
results = [record for record in search_results]
print(f"Number of Records Found: {len(results)}")

# Get one script record
record = results[0]

# Get By ID
record_by_id = ScriptRecord.get_by_id(record.id)
print(f"Record By ID: {record_by_id}")

# Refresh the script record
record.refresh()
print(f"Refreshed Record: {record}")

# Update the script record
record.update(
    script_data={
        "data": "data_updated"
    },
    record_info={
        "test_info": "test_updated"
    },
)

# Create new experiment
new_experiment_name = "Test Experiment B"
new_season_name = "Test Season B"
new_site_name = "Test Site B"

new_experiment = Experiment.create(experiment_name=new_experiment_name)
new_season = new_experiment.create_season(season_name=new_season_name)
new_site = new_experiment.create_site(site_name=new_site_name)

# Update the script record with new experiment, season and site
record.set_experiment(experiment_name=new_experiment_name)
record.set_season(season_name=new_season_name)
record.set_site(site_name=new_site_name)
print(f"Updated Record with new Experiment, Site, Season: {record}")

# Delete the script record
is_deleted = record.delete()
print(f"Deleted Record: {is_deleted}")
