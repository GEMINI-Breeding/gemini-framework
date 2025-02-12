from gemini.api.experiment import Experiment
from gemini.api.season import Season

all_experiments = Experiment.get_all()
for experiment in all_experiments:
    print(experiment)

# Get Experiment A
experiment_a = Experiment.get("Experiment A")
print(experiment_a)

# Get Experiment Seasons
seasons = experiment_a.get_seasons()
print(f"Seasons for Experiment A:")
for season in seasons:
    print(season)

# Create a new Season for Experiment A
new_season = experiment_a.create_season(
    season_name="Season Test A",
    season_start_date="2021-01-01",
    season_end_date="2021-12-31",
    season_info={"test": "test"}
)
print(f"Created Season: {new_season}")

# Get Experiment Sites
sites = experiment_a.get_sites()
print(f"Sites for Experiment A:")
for site in sites:
    print(site)

# Create a new Site for Experiment A
new_site = experiment_a.create_site(
    site_name="Site Test Y",
    site_city="City A",
    site_state="State A",
    site_country="Country A",
    site_info={"test": "test"}
)
print(f"Created Site: {new_site}")


# Get Experiment Cultivars
cultivars = experiment_a.get_cultivars()
print(f"Cultivars for Experiment A:")
for cultivar in cultivars:
    print(cultivar)

# Create a new Cultivar for Experiment A
new_cultivar = experiment_a.create_cultivar(
    cultivar_population="Cultivar Test 2",
    cultivar_accession="Accession A",
    cultivar_info={"test": "test"}
)
print(f"Created Cultivar: {new_cultivar}")

# Get Experiment Datasets
datasets = experiment_a.get_datasets()
print(f"Datasets for Experiment A:")
for dataset in datasets:
    print(dataset)

# Create a new Dataset for Experiment A
new_dataset = experiment_a.create_dataset(
    dataset_name="Dataset Test 2",
    dataset_info={"test": "test"}
)
print(f"Created Dataset: {new_dataset}")

# Get Experiment Traits
traits = experiment_a.get_traits()
print(f"Traits for Experiment A:")
for trait in traits:
    print(trait)


# Create a new Trait for Experiment A
new_trait = experiment_a.create_trait(
    trait_name="Trait Test 1",
    trait_info={"test": "test"}
)
print(f"Created Trait: {new_trait}")

# Get Experiment Models
models = experiment_a.get_models()
print(f"Models for Experiment A:")
for model in models:
    print(model)

# Create a new Model for Experiment A
new_model = experiment_a.create_model(
    model_name="Model Test 1",
    model_info={"test": "test"}
)
print(f"Created Model: {new_model}")

# Get Experiment Sensors
sensors = experiment_a.get_sensors()
print(f"Sensors for Experiment A:")
for sensor in sensors:
    print(sensor)

# Create a new Sensor for Experiment A
new_sensor = experiment_a.create_sensor(
    sensor_name="Sensor Test 2",
    sensor_info={"test": "test"}
)
print(f"Created Sensor: {new_sensor}")

# Get Experiment Procedures
procedures = experiment_a.get_procedures()
print(f"Procedures for Experiment A:")
for procedure in procedures:
    print(procedure)

# Create a new Procedure for Experiment A
new_procedure = experiment_a.create_procedure(
    procedure_name="Procedure Test 2",
    procedure_info={"test": "test"}
)
print(f"Created Procedure: {new_procedure}")

# Get Experiment Sensor Platforms
platforms = experiment_a.get_platforms()
print(f"Sensor Platforms for Experiment A:")
for platform in platforms:
    print(platform)

# Create a new Sensor Platform for Experiment A
new_platform = experiment_a.create_platform(
    platform_name="Sensor Platform Test 2",
    platform_info={"test": "test"}
)
print(f"Created Sensor Platform: {new_platform}")