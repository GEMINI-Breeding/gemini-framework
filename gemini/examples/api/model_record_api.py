from gemini.api.model_record import ModelRecord
from gemini.api.model import Model
from gemini.api.experiment import Experiment
from datetime import datetime, timedelta

# Create a new model for Experiment A
model = Model.create(
    model_name="Test Model A",
    model_info={
        "test_info": "test_value"
    },
    experiment_name="Experiment A"
)
print(f"Created Model: {model}")

# Starting timestamp for the records
starting_timestamp = datetime.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
records_to_add = []

# Create a new model dataset
dataset = model.create_dataset(
    dataset_name="Test Model Dataset A",
    collection_date=starting_timestamp.date(),
    experiment_name="Experiment A"
)
print(f"Created Model Dataset: {dataset}")

# Get valid combinations for the model
valid_combinations = ModelRecord.get_valid_combinations(model_name=model.model_name)
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
        new_model_record = ModelRecord.create(
            model_name=model.model_name,
            dataset_name=dataset.dataset_name,
            experiment_name=experiment_name,
            site_name=site_name,
            season_name=season_name,
            record_info=record_info,
            model_data={
                "data": f"test_data_{i}"
            },
            timestamp=timestamp
        )
        records_to_add.append(new_model_record)
        print(f"Created Model Record: {new_model_record}")
    
    # Increase the starting timestamp for the next combination
    starting_timestamp += timedelta(days=1)

insert_success = ModelRecord.add(records=records_to_add)
print(f"Insert Success: {insert_success}")

# Search for the model records
one_combination = valid_combinations[0]
search_results = ModelRecord.search(
    experiment_name=one_combination['experiment_name'],
    site_name=one_combination['site_name'],
    season_name=one_combination['season_name'],
    model_name=model.model_name,
    dataset_name=one_combination['dataset_name']
)
results = [record for record in search_results]
print(f"Number of Records Found: {len(results)}")

# Get one model record
record = results[0]

# Get By ID
record_by_id = ModelRecord.get_by_id(record.id)
print(f"Record By ID: {record_by_id}")

# Refresh the record
record.refresh()
print(f"Refreshed Record: {record}")

# Update the record
record.update(
    model_data={
        "updated_data": "updated_value"
    },
    record_info={
        "test_info": "updated_test_value"
    },
)

# Update Record Info
record.set_record_info(
    record_info={
        "test_info": "updated_test_value"
    },
)
print(f"Updated Record: {record}")

# Get Record Info
record_info = record.get_record_info()
print(f"Record Info: {record_info}")

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
