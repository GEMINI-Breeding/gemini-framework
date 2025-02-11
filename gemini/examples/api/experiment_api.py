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

# # Get Experiment Sites
# sites = experiment_a.get_sites()
# print(f"Sites for Experiment A:")
# for site in sites:
#     print(site)

# # Get Experiment Cultivars
# cultivars = experiment_a.get_cultivars()
# print(f"Cultivars for Experiment A:")
# for cultivar in cultivars:
#     print(cultivar)

# # Get Experiment Datasets
# datasets = experiment_a.get_datasets()
# print(f"Datasets for Experiment A:")
# for dataset in datasets:
#     print(dataset)

# # Get Experiment Traits
# traits = experiment_a.get_traits()
# print(f"Traits for Experiment A:")
# for trait in traits:
#     print(trait)

# # Get Experiment Models
# models = experiment_a.get_models()
# print(f"Models for Experiment A:")
# for model in models:
#     print(model)

# # Get Experiment Sensors
# sensors = experiment_a.get_sensors()
# print(f"Sensors for Experiment A:")
# for sensor in sensors:
#     print(sensor)

# # Get Experiment Procedures
# procedures = experiment_a.get_procedures()
# print(f"Procedures for Experiment A:")
# for procedure in procedures:
#     print(procedure)

# # Get Experiment Sensor Platforms
# platforms = experiment_a.get_platforms()
# print(f"Sensor Platforms for Experiment A:")
# for platform in platforms:
#     print(platform)