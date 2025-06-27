from gemini.api.season import Season

# Create a new Season for Experiment A
new_season = Season.create(
    season_name="Season 1A",
    season_year=2024,
    season_info={"notes": "First season of Experiment A"},
    experiment_name="Experiment A"
)
print(f"Created New Season: {new_season}")

# Get Season by ID
season_by_id = Season.get_by_id(new_season.id)
print(f"Got Season by ID: {season_by_id}")

# Get Season by Name
season_by_name = Season.get(season_name="Season 1A")
print(f"Got Season by Name: {season_by_name}")

# Get all Seasons
all_seasons = Season.get_all()
for season in all_seasons:
    print(f"Season: {season}")

# Search for Seasons by Name
search_results = Season.search(season_name="Season 1A")
for result in search_results:
    print(f"Search Result: {result}")

# Update Season
season_by_name.update(
    season_year=2025
)
print(f"Updated Season: {season_by_name}")

# Refresh Season
season_by_name.refresh()
print(f"Refreshed Season: {season_by_name}")

# Set Season Info
season_by_name.set_info(
    season_info={"notes": "Updated notes for Season 1A"}
)
print(f"Set Season Info: {season_by_name.get_info()}")

# Check if Season Exists
exists = Season.exists(season_name="Season 1A")
print(f"Does Season Exist? {exists}")

# Delete Season
is_deleted = season_by_name.delete()
print(f"Deleted Season: {is_deleted}")

# Check if Season Exists after Deletion
exists_after_deletion = Season.exists(season_name="Season 1A")
print(f"Does Season Exist after Deletion? {exists_after_deletion}")
