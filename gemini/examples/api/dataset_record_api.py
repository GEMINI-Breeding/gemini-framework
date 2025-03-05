from gemini.api.dataset_record import DatasetRecord
from gemini.api.dataset import Dataset
from gemini.api.experiment import Experiment
from datetime import datetime, timedelta

# Create a new dataset for Experiment A
dataset = Dataset.create(
    dataset_name="Test Dataset A",
    dataset_info={
        "test_info": "test_value"
    },
    experiment_name="Experiment A"
)
print(f"Created Dataset: {dataset}")

# Starting timestamp for the records
starting_timestamp = datetime.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
records_to_add = []

# Get valid combinations for the dataset
valid_combinations = DatasetRecord.get_valid_combinations(dataset_name=dataset.dataset_name)
print(f"Valid Combinations: {valid_combinations}")
print(f"Number of Valid Combinations: {len(valid_combinations)}")

# For each valid combination, add records
for valid_combination in valid_combinations:
    experiment_name = valid_combination['experiment_name']
    site_name = valid_combination['site_name']
    season_name = valid_combination['season_name']
    record_info = {
        "test_info": "test_value"
    }
    for i in range(10):
        timestamp = starting_timestamp + timedelta(minutes=i)
        record_info = {
            "test_info": f"test_value_{i}"
        }
        new_dataset_record = DatasetRecord.create(
            dataset_name=dataset.dataset_name,
            experiment_name=experiment_name,
            site_name=site_name,
            season_name=season_name,
            record_info=record_info,
            dataset_data={
                "data": f"test_data_{i}"
            },
            timestamp=timestamp
        )
        records_to_add.append(new_dataset_record)
        print(f"Created Dataset Record: {new_dataset_record}")
    
    # Increase the starting timestamp for the next combination
    starting_timestamp += timedelta(days=1)

insert_success = DatasetRecord.add(records=records_to_add)
print(f"Insert Success: {insert_success}")

# Search for the dataset records
one_combination = valid_combinations[0]
search_results = DatasetRecord.search(
    experiment_name=one_combination['experiment_name'],
    site_name=one_combination['site_name'],
    season_name=one_combination['season_name'],
    dataset_name=dataset.dataset_name
)
results = [record for record in search_results]
print(f"Number of Records Found: {len(results)}")

# Get one dataset record
record = results[0]

# Get By ID
record_by_id = DatasetRecord.get_by_id(record.id)
print(f"Record By ID: {record_by_id}")

# Refresh the record
record.refresh()
print(f"Refreshed Record: {record}")

# Update the record
record.update(
    dataset_data={
        "updated_data": "updated_value"
    },
    record_info={
        "test_info": "updated_test_value"
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
