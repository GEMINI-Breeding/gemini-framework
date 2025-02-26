from gemini.api.experiment import Experiment
from gemini.api.enums import GEMINIDataFormat, GEMINIDatasetType, GEMINIDataType, GEMINISensorType, GEMINITraitLevel

# Create a new experiment
new_experiment = Experiment.create(
    experiment_name="Experiment Test 1",
    experiment_info={"test": "test"},
    experiment_start_date="2023-10-01",
    experiment_end_date="2023-10-02",
)
print(f"Created Experiment: {new_experiment}")

# Get Experiment with experiment_name that does exist
experiment = Experiment.get("Experiment Test 1")
print(f"Got Experiment: {experiment}")

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
print(f"Found {length_searched_experiments} experiments")

# Update the experiment
experiment.update(
    experiment_info={"test": "test_updated"},
)
print(f"Updated Experiment: {experiment}")

# Refresh the experiment
experiment.refresh()
print(f"Refreshed Experiment: {experiment}")

# Delete the experiment
experiment.delete()
print(f"Deleted Experiment: {experiment}")

# Get Experiment A
experiment_a = Experiment.get("Experiment A")
print(f"Got Experiment A: {experiment_a}")

# Get Experiment Seasons
experiment_seasons = experiment_a.get_seasons()
print(f"Got Experiment Seasons: {experiment_seasons}")

# Get Experiment Cultivars
experiment_cultivars = experiment_a.get_cultivars()
print(f"Got Experiment Cultivars: {experiment_cultivars}")

# Get Experiment Sites
experiment_sites = experiment_a.get_sites()
print(f"Got Experiment Sites: {experiment_sites}")

# Get Experiment Sensors
experiment_sensors = experiment_a.get_sensors()
print(f"Got Experiment Sensors: {experiment_sensors}")

# Get Experiment Datasets
experiment_datasets = experiment_a.get_datasets()
print(f"Got Experiment Datasets: {experiment_datasets}")

# Get Experiment Traits
experiment_traits = experiment_a.get_traits()
print(f"Got Experiment Traits: {experiment_traits}")

# Get Experiment Models
experiment_models = experiment_a.get_models()
print(f"Got Experiment Models: {experiment_models}")

# Get Experiment Scripts
experiment_scripts = experiment_a.get_scripts()
print(f"Got Experiment Scripts: {experiment_scripts}")

# Get Experiment Procedures
experiment_procedures = experiment_a.get_procedures()
print(f"Got Experiment Procedures: {experiment_procedures}")

# Get Experiment Sensor Platforms
experiment_sensor_platforms = experiment_a.get_platforms()
print(f"Got Experiment Sensor Platforms: {experiment_sensor_platforms}")

# Create a new season for the experiment
new_season = experiment_a.create_season(
    season_name="Season Test 1",
    season_info={"test": "test"},
    season_start_date="2023-10-01",
    season_end_date="2023-10-02",
)
print(f"Created Season: {new_season}")

# Create a new cultivar for the experiment
new_cultivar = experiment_a.create_cultivar(
    cultivar_accession="Test Accession",
    cultivar_population="Test Population",
    cultivar_info={"test": "test"},
)
print(f"Created Cultivar: {new_cultivar}")

# Create a new site for the experiment
new_site = experiment_a.create_site(
    site_name="Test Site",
    site_city="Test City",
    site_state="Test State",
    site_country="Test Country",
    site_info={"test": "test"},
)
print(f"Created Site: {new_site}")

# Create a new sensor platform for the experiment
new_platform = experiment_a.create_platform(
    platform_name="Test Platform",
    platform_info={"test": "test"},
)

# Create a new sensor for the experiment
new_sensor = experiment_a.create_sensor(
    sensor_name="Test Sensor",
    sensor_type=GEMINISensorType.RGB,
    sensor_data_format=GEMINIDataFormat.JPEG,
    sensor_data_type=GEMINIDataType.IMAGE,
    sensor_info={"test": "test"}
)