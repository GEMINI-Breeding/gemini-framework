from gemini.api.experiment import Experiment
from gemini.api.sensor import GEMINIDataFormat, GEMINISensorType, GEMINIDataType
from gemini.api.dataset import GEMINIDatasetType
from gemini.api.trait import GEMINITraitLevel

# Get Experiment A
experiment = Experiment.get("Experiment A")
print(f"Got Experiment: {experiment}")

# Get Experiment Seasons
experiment_seasons = experiment.get_seasons()
print(f"Experiment Seasons:")
for season in experiment_seasons:
    print(season)

# Get Experiment Cultivars
experiment_cultivars = experiment.get_cultivars()
print(f"Experiment Cultivars:")
for cultivar in experiment_cultivars:
    print(cultivar)

# Get Experiment Sensor Platforms
experiment_sensor_platforms = experiment.get_platforms()
print(f"Experiment Sensor Platforms:")
for platform in experiment_sensor_platforms:
    print(platform)


# Get Experiment Sensors
experiment_sensors = experiment.get_sensors()
print(f"Experiment Sensors:")
for sensor in experiment_sensors:
    print(sensor)

# Get Experiment Traits
experiment_traits = experiment.get_traits()
print(f"Experiment Traits:")
for trait in experiment_traits:
    print(trait)

# Get Experiment Scripts
experiment_scripts = experiment.get_scripts()
print(f"Experiment Scripts:")
for script in experiment_scripts:
    print(script)

# Get Experiment Procedures
experiment_procedures = experiment.get_procedures()
print(f"Experiment Procedures:")
for procedure in experiment_procedures:
    print(procedure)

# Get Experiment Models
experiment_models = experiment.get_models()
print(f"Experiment Models:")
for model in experiment_models:
    print(model)


# Get Experiment Datasets
experiment_datasets = experiment.get_datasets()
print(f"Experiment Datasets:")
for dataset in experiment_datasets:
    print(dataset)

# Create new experiment
new_experiment = Experiment.create(
    experiment_name="Experiment Test 1",
    experiment_info={"test": "test"},
    experiment_start_date="2023-10-01",
    experiment_end_date="2023-10-31"
)
print(f"Created Experiment: {new_experiment}")

# Get Experiment by ID
experiment = Experiment.get_by_id(new_experiment.id)
print(f"Got Experiment by ID: {experiment}")

# Get all experiments
all_experiments = Experiment.get_all()
print(f"All Experiments:")
for experiment in all_experiments:
    print(experiment)

# Search for experiments
searched_experiments = Experiment.search(experiment_name="Experiment Test 1")
length_searched_experiments = len(searched_experiments)
print(f"Found {length_searched_experiments} experiments with name 'Experiment Test 1'")

# Refresh the experiment
experiment.refresh()
print(f"Refreshed Experiment: {experiment}")

# Update the experiment
experiment.update(
    experiment_info={"test": "test_updated"},
    experiment_start_date="2023-11-01",
    experiment_end_date="2023-11-30"
)
print(f"Updated Experiment: {experiment}")

# Add a new season for the experiment
new_season = experiment.create_season(
    season_name="Season Test 1",
    season_start_date="2023-10-01",
    season_end_date="2023-10-31",
    season_info={"test": "test"}
)
print(f"Created Season: {new_season}")

# Add a new cultivar for the experiment
new_cultivar = experiment.create_cultivar(
    cultivar_accession="Cultivar Test 1",
    cultivar_population="Population Test 1",
    cultivar_info={"test": "test"}
)
print(f"Created Cultivar: {new_cultivar}")

# Add a new sensor platform for the experiment
new_sensor_platform = experiment.create_platform(
    platform_name="Sensor Platform Test 1",
    platform_info={"test": "test"}
)
print(f"Created Sensor Platform: {new_sensor_platform}")

# Add a new sensor for the experiment
new_sensor = experiment.create_sensor(
    sensor_name="Sensor Test 1",
    sensor_info={"test": "test"},
    sensor_data_format=GEMINIDataFormat.CSV,
    sensor_data_type=GEMINIDataType.Binary,
    sensor_type=GEMINISensorType.Calibration,
    sensor_platform_name=new_sensor_platform.sensor_platform_name
)
print(f"Created Sensor: {new_sensor}")

# Add a new trait for the experiment
new_trait = experiment.create_trait(
    trait_name="Trait Test 1",
    trait_info={"test": "test"},
    trait_level=GEMINITraitLevel.Plant,
    trait_metrics={"metric1": "value1", "metric2": "value2"},
    trait_units="units"
)
print(f"Created Trait: {new_trait}")

# Add a new script for the experiment
new_script = experiment.create_script(
    script_name="Script Test 1",
    script_url="https://example.com/script",
    script_extension=".py",
    script_info={"test": "test"}
)
print(f"Created Script: {new_script}")

# Add a new procedure for the experiment
new_procedure = experiment.create_procedure(
    procedure_name="Procedure Test 1",
    procedure_info={"test": "test"}
)
print(f"Created Procedure: {new_procedure}")

# Add a new model for the experiment
new_model = experiment.create_model(
    model_name="Model Test 1",
    model_info={"test": "test"},
    model_url="https://example.com/model",
)
print(f"Created Model: {new_model}")    


# Add a new Site
new_site = experiment.create_site(
    site_name="Site Test 1",
    site_city="City Test 1",
    site_state="State Test 1",
    site_country="Country Test 1",
    site_info={"test": "test"}
)
print(f"Created Model: {new_model}")

# Add a new dataset for the experiment
new_dataset = experiment.create_dataset(
    dataset_name="Dataset Test 1",
    dataset_info={"test": "test"},
    dataset_type=GEMINIDatasetType.Script,
    collection_date="2023-10-01"
)
print(f"Created Dataset: {new_dataset}")

# Delete the experiment
is_deleted = experiment.delete()
print(f"Deleted Experiment: {is_deleted}")