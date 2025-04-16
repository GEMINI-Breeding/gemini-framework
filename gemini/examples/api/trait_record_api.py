from gemini.api.trait_record import TraitRecord
from gemini.api.trait import Trait, GEMINITraitLevel
from gemini.api.plot import Plot
from datetime import datetime, timedelta

from gemini.api.experiment import Experiment

# Create a new trait for Experiment A
trait = Trait.create(
    trait_name="Test Trait A",
    trait_units="units",
    trait_level=GEMINITraitLevel.Plot,
    trait_info={"test": "test", "test2": "test2"},
    trait_metrics={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created Trait: {trait}")



# Starting timestamp for the records
starting_timestamp = datetime.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
records_to_add = []

# Create a new trait dataset
dataset = trait.create_dataset(
    dataset_name="Test Dataset A",
    collection_date=starting_timestamp.date(),
    experiment_name="Experiment A"
)
print(f"Created Trait Dataset: {dataset}")

# Get valid combinations for the trait
valid_combinations = TraitRecord.get_valid_combinations(trait_name=trait.trait_name)
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
    plot = Plot.get(
        experiment_name=experiment_name,
        site_name=site_name,
        season_name=season_name,
        plot_number=1,
        plot_row_number=1,
        plot_column_number=1,
    )

    for i in range(10):
        timestamp = starting_timestamp + timedelta(minutes=i)
        record_info = {
            "test_info": f"test_value_{i}"
        }
        new_trait_record = TraitRecord.create(
            experiment_name=experiment_name,
            site_name=site_name,
            season_name=season_name,
            trait_name=trait.trait_name,
            dataset_name=dataset.dataset_name,
            record_info=record_info,
            plot_column_number=plot.plot_column_number,
            plot_row_number=plot.plot_row_number,
            plot_number=plot.plot_number,
            trait_value=10 + i,
            timestamp=timestamp
        )
        print(f"Created Trait Record: {new_trait_record}")
        # Add the trait record
        records_to_add.append(new_trait_record)
    # Increase the starting timestamp for the next combination
    starting_timestamp += timedelta(days=1)

insert_success = TraitRecord.add(records=records_to_add)
print(f"Insert Success: {insert_success}")

# Search for trait records
one_combination = valid_combinations[0]
search_results = TraitRecord.search(
    experiment_name=one_combination['experiment_name'],
    site_name=one_combination['site_name'],
    season_name=one_combination['season_name'],
    trait_name=trait.trait_name,
    dataset_name=one_combination['dataset_name']
)
results = [record for record in search_results]
print(f"Number of Records Found: {len(results)}")

# Get one trait record
record = results[0]

# Get By ID
record_by_id = TraitRecord.get_by_id(record.id)
print(f"Record By ID: {record_by_id}")

# Refresh the record
record.refresh()
print(f"Refreshed Record: {record}")

# Update the record
record.update(
    record_info={
        "test_info": "updated_test_value"
    },
    trait_value=9999
)
print(f"Updated Record: {record}")

# Set Trait Record Info
record.set_record_info(
    record_info={
        "test_info": "set_test_value"
    },
)
print(f"Set Record Info: {record}")

# Get Record Info
record_info = record.get_record_info()
print(f"Record Info: {record_info}")

# Create a new experiment
new_experiment_name = "Test Experiment B"
new_season_name = "Test Season B"
new_site_name = "Test Site B"

new_experiment = Experiment.create(experiment_name=new_experiment_name)
new_season = new_experiment.create_season(season_name=new_season_name)
new_site = new_experiment.create_site(site_name=new_site_name)

# Update the record with new experiment, season and site
record.set_experiment(experiment_name=new_experiment_name)
record.set_season(season_name=new_season_name)
record.set_site(site_name=new_site_name)

# Create a new plot
new_plot = Plot.create(
    plot_number=1,
    plot_row_number=1,
    plot_column_number=1,
    experiment_name=new_experiment_name,
    site_name=new_site_name,
    season_name=new_season_name
)

# Update the record with new plot
record.set_plot(
    plot_number=new_plot.plot_number,
    plot_row_number=new_plot.plot_row_number,
    plot_column_number=new_plot.plot_column_number,
)
print(f"Updated Record with new Experiment, Site, Season, Plot: {record}")

# Delete the record
is_deleted = record.delete()
print(f"Is Deleted: {is_deleted}")










# trait_name = 'Trait A1'
# starting_timestamp = datetime.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
# records_to_add = []

# valid_combinations = TraitRecord.get_valid_combinations(trait_name=trait_name)
# print(f"Valid Combinations: {valid_combinations}")

# for valid_combination in valid_combinations:
#     dataset_name = valid_combination['dataset_name']
#     experiment_name = valid_combination['experiment_name']
#     site_name = valid_combination['site_name']
#     season_name = valid_combination['season_name']
#     plots = Plot.search( 
#         experiment_name=experiment_name,
#         site_name=site_name,
#         season_name=season_name,
#     )

#     for i in range(10):
#         plot = plots[0]
#         timestamp = starting_timestamp + timedelta(minutes=i)
#         record_info = {
#             "test_info": f"test_value_{i}"
#         }
#         new_trait_record = TraitRecord.create(
#             experiment_name=experiment_name,
#             site_name=site_name,
#             season_name=season_name,
#             trait_name=trait_name,
#             dataset_name=dataset_name,
#             record_info=record_info,
#             plot_column_number=plot.plot_column_number,
#             plot_row_number=plot.plot_row_number,
#             plot_number=plot.plot_number,
#             trait_value = 10*i,
#             timestamp=timestamp
#         )
#         print(f"Created Trait Record: {new_trait_record}")

#         # Add the trait record
#         records_to_add.append(new_trait_record)

#     # Increase the starting timestamp for the next combination
#     starting_timestamp += timedelta(days=1)

# # Add the trait records to the database
# insert_success = TraitRecord.add(records=records_to_add)
# print(f"Insert Success: {insert_success}")

# # Search for the trait records
# one_combination = valid_combinations[0]
# search_results = TraitRecord.search(
#     experiment_name=one_combination['experiment_name'],
#     site_name=one_combination['site_name'],
#     season_name=one_combination['season_name'],
#     trait_name=trait_name,
#     dataset_name=one_combination['dataset_name']
# )
# results = [record for record in search_results]
# print(f"Number of Records Found: {len(results)}")
