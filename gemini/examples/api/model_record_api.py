from gemini.api.model_record import ModelRecord
from datetime import datetime, timedelta

model_name = 'Model A'
# dataset_name = 'New Dataset for Model A'
starting_timestamp = datetime.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
records_to_add = []

valid_combinations = ModelRecord.get_valid_combinations(model_name=model_name)
print(f"Valid Combinations: {valid_combinations}")

# For each combination add 100 records
for valid_combination in valid_combinations:
    experiment_name = valid_combination['experiment_name']
    site_name = valid_combination['site_name']
    season_name = valid_combination['season_name']
    dataset_name = valid_combination['dataset_name']
    record_info = {
        "test_info": "test_value"
    }
    for i in range(100):
        new_model_record = ModelRecord.create(
            experiment_name=experiment_name,
            site_name=site_name,
            season_name=season_name,
            model_name=model_name,
            dataset_name=dataset_name,
            record_info=record_info,
            model_data={
                "data": "data_" + str(i)
            },
            timestamp=starting_timestamp + timedelta(minutes=i)
        )
        print(f"Created Model Record: {new_model_record}")

        # Add the model record
        records_to_add.append(new_model_record)

# Add the model records to the database
insert_success = ModelRecord.add(records=records_to_add)
print(f"Insert Success: {insert_success}")

# Search for the model records
one_combination = valid_combinations[0]
search_results = ModelRecord.search(
    experiment_name=one_combination['experiment_name'],
    site_name=one_combination['site_name'],
    season_name=one_combination['season_name'],
    model_name=model_name,
    dataset_name=one_combination['dataset_name'],
    collection_date=starting_timestamp.date()
)
results = [record for record in search_results]
print(f"Search Results: {results}")

# Get one model record
record = results[0]

# Get By ID
record_by_id = ModelRecord.get_by_id(record.id)
print(f"Record By ID: {record_by_id}")

# Refresh the record
record.refresh()
print(f"Refreshed Record: {record}")

# Get the last valid combination
last_valid_combination = valid_combinations[-1]
# Update the record
record.update(
    record_info={"test_info": "test_value_updated"},
    model_data={"data": "data_updated"}
)
print(f"Updated Record: {record}")

# Update experiment, season and site
record.set_experiment(experiment_name=last_valid_combination['experiment_name'])
record.set_season(season_name=last_valid_combination['season_name'])
record.set_site(site_name=last_valid_combination['site_name'])
print(f"Updated Record: {record}")

# Delete the record
is_deleted = record.delete()
print(f"Deleted Record: {is_deleted}")



