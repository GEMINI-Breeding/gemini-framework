from gemini.api.experiment import Experiment

# Get Experiment A
experiment_a = Experiment.get("Experiment A")
print(f"Got Experiment A: {experiment_a}")

# Get Associated Seasons
associated_seasons = experiment_a.get_associated_seasons()
for season in associated_seasons:
    print(f"Associated Season: {season}")

# Create a new season for Experiment A
new_experiment_season = experiment_a.create_new_season(
    season_name="Experiment A Season 1",
    season_info={"test": "test"},
    season_start_date="2023-10-01",
    season_end_date="2023-12-31"
)
print(f"Created New Season: {new_experiment_season}")

# Get Associated Seasons for Experiment A
associated_seasons = experiment_a.get_associated_seasons()
for season in associated_seasons:
    print(f"Associated Season: {season}")
