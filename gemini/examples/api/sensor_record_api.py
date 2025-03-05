from gemini.api.sensor_record import SensorRecord
from gemini.api.sensor import Sensor
from gemini.api.plot import Plot
from datetime import datetime, timedelta

from gemini.api.experiment import Experiment        

# Create a new sensor for Experiment A
sensor = Sensor.create(
    sensor_name="Test Sensor A",
    sensor_info={
        "test_info": "test_value"
    },
    experiment_name="Experiment A"
)
print(f"Created Sensor: {sensor}")

# Starting timestamp for the records
starting_timestamp = datetime.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
records_to_add = []

# Create a new sensor dataset
dataset = sensor.create_dataset(
    dataset_name="Test Sensor Dataset A",
    collection_date=starting_timestamp.date(),
    experiment_name="Experiment A"
)
print(f"Created Sensor Dataset: {dataset}")

# Get valid combinations for the sensor
valid_combinations = SensorRecord.get_valid_combinations(sensor_name=sensor.sensor_name)
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
        new_sensor_record = SensorRecord.create(
            experiment_name=experiment_name,
            site_name=site_name,
            season_name=season_name,
            sensor_name=sensor.sensor_name,
            dataset_name=dataset.dataset_name,
            record_info=record_info,
            plot_column_number=plot.plot_column_number,
            plot_row_number=plot.plot_row_number,
            plot_number=plot.plot_number,
            sensor_data={
                "data": f"sensor_data_{i}"
            },
            timestamp=timestamp
        )
        print(f"Created Sensor Record: {new_sensor_record}")
        # Add the record to the list
        records_to_add.append(new_sensor_record)
    # Increase the starting timestamp for the next combination
    starting_timestamp += timedelta(days=1)

insert_success = SensorRecord.add(records=records_to_add)
print(f"Insert Success: {insert_success}")

# Search for the sensor records
one_combination = valid_combinations[0]
search_results = SensorRecord.search(
    experiment_name=one_combination['experiment_name'],
    site_name=one_combination['site_name'],
    season_name=one_combination['season_name'],
    sensor_name=sensor.sensor_name,
    dataset_name=dataset.dataset_name
)
results = [record for record in search_results]
print(f"Number of Records Found: {len(results)}")

# Get one sensor record
record = results[0]

# Get By ID
record_by_id = SensorRecord.get_by_id(record.id)
print(f"Record By ID: {record_by_id}")

# Refresh the record
record.refresh()
print(f"Refreshed Record: {record}")

# Update the record
record.update(
    record_info = {"test_info": "test_value_updated"},
    sensor_data = {"data": "sensor_data_updated"}
)
print(f"Updated Record: {record}")

# Create a new experiment
new_experiment_name = "Test Experiment B"
new_season_name = "Test Season B"
new_site_name = "Test Site B"

new_experiment = Experiment.create(experiment_name=new_experiment_name)
new_season = new_experiment.create_season(season_name=new_season_name)
new_site = new_experiment.create_site(site_name=new_site_name)

# Set the new experiment, season and site for the record
record.set_experiment(experiment_name=new_experiment_name)
record.set_season(season_name=new_season_name)
record.set_site(site_name=new_site_name)

# Create a new plot
new_plot = Plot.create(
    plot_number=1,
    plot_row_number=1,
    plot_column_number=1,
    experiment_name=new_experiment_name,
    season_name=new_season_name,
    site_name=new_site_name
)

# Set the new plot for the record
record.set_plot(
    plot_number=new_plot.plot_number,
    plot_row_number=new_plot.plot_row_number,
    plot_column_number=new_plot.plot_column_number
)
print(f"Updated Record with New Plot: {record}")

# Delete the record
is_deleted = record.delete()
print(f"Record Deleted: {is_deleted}")