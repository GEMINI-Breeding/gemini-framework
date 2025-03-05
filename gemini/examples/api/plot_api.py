from gemini.api.plot import Plot
from gemini.api.cultivar import Cultivar
from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site

from random import choice
from tqdm import tqdm

valid_combinations = Plot.get_valid_combinations()
print(f"Valid Combinations: {valid_combinations}")

# Remove valid_combinations with experiment_name GEMINI
valid_combinations = [combination for combination in valid_combinations if combination['experiment_name'] != 'GEMINI']


starting_plot_number = 10000
starting_plot_row_number = 1000
starting_plot_column_number = 1000

all_cultivars = Cultivar.get_all()
print(f"Number of Cultivars: {len(all_cultivars)}")

created_plots = []

# For each combination create 10 plots
for valid_combination in tqdm(valid_combinations, desc="Creating Plots", unit="combination"):
    experiment_name = valid_combination['experiment_name']
    site_name = valid_combination['site_name']
    season_name = valid_combination['season_name']
    plot_info = {
        "test_info": "test_value"
    }
    plot_geometry_info = {
        "geometry": "geometry_value"
    }

    # Randomly select a cultivar
    experiment_cultivars = Experiment.get(experiment_name=experiment_name).get_cultivars()
    random_cultivar = choice(experiment_cultivars) if experiment_cultivars else None

    for i in range(10):
        new_plot = Plot.create(
            experiment_name=experiment_name,
            site_name=site_name,
            season_name=season_name,
            plot_number=starting_plot_number + i,
            plot_row_number=starting_plot_row_number + i,
            plot_column_number=starting_plot_column_number + i,
            plot_info=plot_info,
            plot_geometry_info=plot_geometry_info,
            cultivar_accession=random_cultivar.cultivar_accession if random_cultivar else None,
            cultivar_population=random_cultivar.cultivar_population if random_cultivar else None,
        )
        created_plots.append(new_plot)

print(f"Created Plots: {created_plots}")

# Get a plot based on some valid combination and number
plot = Plot.get(
    plot_number = 10005,
    plot_row_number = 1005,
    plot_column_number= 1005,
    experiment_name=valid_combinations[-1]['experiment_name'],
    site_name=valid_combinations[-1]['site_name'],
    season_name=valid_combinations[-1]['season_name']
)
print(f"Plot: {plot}")

# Get Plot by ID
plot_by_id = Plot.get_by_id(plot.id)
print(f"Plot by ID: {plot_by_id}")

# Get all plots
all_plots = Plot.get_all()
print(f"Length of all plots: {len(all_plots)}")

# Search for plots
searched_plots = Plot.search(
    experiment_name=valid_combinations[-1]['experiment_name'],
    site_name=valid_combinations[-1]['site_name'],
    season_name=valid_combinations[-1]['season_name'],
)
print(f"Length of searched plots: {len(searched_plots)}")

# Refresh the plot
plot.refresh()
print(f"Refreshed Plot: {plot}")

# Update the plot
plot.update(
    plot_number=20000,
    plot_row_number=2000,
    plot_column_number=2000,
    plot_info={"test_info": "updated_test_value"},
    plot_geometry_info={"geometry": "updated_geometry_value"},
)
print(f"Updated Plot: {plot}")

# Add a new cultivar
experiment_cultivars = Experiment.get(experiment_name=valid_combinations[-1]['experiment_name']).get_cultivars()
random_cultivar = choice(experiment_cultivars) if experiment_cultivars else None
plot.add_cultivar(
    cultivar_accession=random_cultivar.cultivar_accession if random_cultivar else None,
    cultivar_population=random_cultivar.cultivar_population if random_cultivar else None,
    cultivar_info={"test_info": "test_value"}
)

# Get cultivar from plot
cultivars = plot.get_cultivars()
print(f"Cultivars from Plot: {cultivars}")

# Get another valid combination
valid_combination = Plot.get_valid_combinations()[0]
new_experiment_name = valid_combination['experiment_name']
new_site_name = valid_combination['site_name']
new_season_name = valid_combination['season_name']

# Update the plot with a new valid combination
plot.set_experiment(experiment_name=new_experiment_name)
plot.set_site(site_name=new_site_name)
plot.set_season(experiment_name=new_experiment_name, season_name=new_season_name)
print(f"Updated Plot with new valid combination: {plot}")

# Get new experiment's cultivars
new_experiment_cultivars = Experiment.get(experiment_name=new_experiment_name).get_cultivars()

# Add 5 plants
for i in range(5):
    plot.add_plant(
        plant_number=starting_plot_number + i,
        cultivar_accession=new_experiment_cultivars[i % len(new_experiment_cultivars)].cultivar_accession,
        cultivar_population=new_experiment_cultivars[i % len(new_experiment_cultivars)].cultivar_population,
        plant_info={"test_info": "test_value"}
    )
print(f"Added Plants to Plot: {plot}")

# Get Plants
plants = plot.get_plants()
print(f"Plants from Plot: {plants}")

# Delete the plot
is_deleted = plot.delete()
print(f"Deleted Plot: {is_deleted}")



