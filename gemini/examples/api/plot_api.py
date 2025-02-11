from gemini.api.plot import Plot
import random

# Get all plots
all_plots = Plot.get_all()

# Get 5 random plots from all_plots array
random_plots = random.sample(all_plots, 5)
for plot in random_plots:
    print(f"Plot ID: {plot.id}, Plot Number: {plot.plot_number}, Plot Row Number: {plot.plot_row_number}, Plot Column Number: {plot.plot_column_number}")

# For each plot, get the plants
for plot in random_plots:
    plants = plot.get_plants()
    print(f"Plants for Plot ID {plot.id}:")
    for plant in plants:
        print(f"Plant ID: {plant.id}, Plant Number: {plant.plant_number}")

# For each plot, get the cultivars
for plot in random_plots:
    cultivars = plot.get_cultivars()
    print(f"Cultivars for Plot ID {plot.id}:")
    for cultivar in cultivars:
        print(f"Cultivar ID: {cultivar.id}, Cultivar Accession: {cultivar.cultivar_accession}, Cultivar Population: {cultivar.cultivar_population}")

# For each plot, get the experiment, season, and site
for plot in random_plots:
    experiment = plot.get_experiment()
    season = plot.get_season()
    site = plot.get_site()
    print(f"Plot ID {plot.id} is in Experiment {experiment.experiment_name}, Season {season.season_name}, Site {site.site_name}")

# Plot Search
searched_plots = Plot.search(experiment_name="Experiment A")
length_searched_plots = len(searched_plots)
print(f"Found {length_searched_plots} plots in Experiment A")

searched_plots = Plot.search(site_name="Site A")
length_searched_plots = len(searched_plots)
print(f"Found {length_searched_plots} plots in Site A")

searched_plots = Plot.search(experiment_name="Experiment A", site_name="Site A")
length_searched_plots = len(searched_plots)
print(f"Found {length_searched_plots} plots in Experiment A and Site A")