from gemini.db.models.seasons import SeasonModel

# Get all seasons
seasons = SeasonModel.all()

# Get one of the seasons
season = seasons[0]

# Print plots for the season
print("Plots:")
plots = season.plots
for plot in plots:
    print(plot.plot_number)

# For each season, print experiment name
for season in seasons:
    experiment = season.experiment
    print(f"Experiment: {experiment.experiment_name}")