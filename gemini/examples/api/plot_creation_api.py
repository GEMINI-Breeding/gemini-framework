from gemini.api.plot import Plot
from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site

# Get Experiment A
experiment_a = Experiment.get("Experiment A")
experiment_a_seasons = experiment_a.get_seasons()

# Get First Season
first_season = experiment_a_seasons[0]

# Get Site A
site_a = Site.get("Site A")

# Number of plots to create
number_of_plots = 100
starting_plot_number = 900
starting_plot_row_number = 900
starting_plot_column_number = 900

# Create plots
for i in range(number_of_plots):
    plot = Plot.create(
        plot_number=i,
        plot_row_number=i,
        plot_column_number=i,
        experiment_name=experiment_a.experiment_name,
        season_name=first_season.season_name,
        site_name=site_a.site_name
    )
    print(f"Created Plot {plot.plot_number}")
