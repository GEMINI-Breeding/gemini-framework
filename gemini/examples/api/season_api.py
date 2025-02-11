from gemini.api.season import Season
from gemini.api.experiment import Experiment

# Create a new season with an experiment name that does exist
new_season = Season.create(
    season_name="Season Test C",
    season_start_date="2021-01-01",
    season_end_date="2021-12-31",
    season_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created Season: {new_season}")

# Get Season with season_name and experiment_name that do exist
season = Season.get("Season Test C", "Experiment A")
print(f"Got Season: {season}")

# Get Season by ID
season = Season.get_by_id(new_season.id)
print(f"Got Season by ID: {season}")

# Get all seasons
all_seasons = Season.get_all()
print(f"All Seasons:")
for season in all_seasons:
    print(season)

# Search for seasons
searched_seasons = Season.search(experiment_name="Experiment A")
length_searched_seasons = len(searched_seasons)
print(f"Found {length_searched_seasons} seasons in Experiment A")

# Refresh the season
season = season.refresh()
print(f"Refreshed Season: {season}")