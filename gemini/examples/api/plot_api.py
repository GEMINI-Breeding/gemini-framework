from gemini.api.plot import Plot
from gemini.api.cultivar import Cultivar
from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site

# Get all plots
plots = Plot.get_all()
print(f"All Plots:")
for plot in plots:
    print(plot)
print(f"Number of Plots: {len(plots)}")

# Create a new experiment, season and site for testing
experiment = Experiment.create(experiment_name="Test Experiment")
season = Season.create(season_name="Test Season", experiment_name=experiment.experiment_name)
site = Site.create(
    site_name="Test Site",
    site_city="Test City",
    site_state="Test State",
    site_country="Test Country",
    site_info={"info": "info"},
    experiment_name=experiment.experiment_name,
)

print(f"New Experiment: {experiment}")
print(f"New Season: {season}")
print(f"New Site: {site}")

# Create a new cultivar
cultivar = Cultivar.create(
    cultivar_accession="Test Accession",
    cultivar_population="Test Population",
    experiment_name=experiment.experiment_name,
    cultivar_info={"info": "info"}
)
print(f"New Cultivar: {cultivar}")


# Create a new plot
new_plot = Plot.create(
    plot_number=99,
    plot_column_number=99,
    plot_row_number=99,
    experiment_name=experiment.experiment_name,
    season_name=season.season_name,
    site_name=site.site_name,
)
print(f"New Plot: {new_plot}")

# Get plot from ID
plot = Plot.get_by_id(new_plot.id)
print(f"Plot from ID: {plot}")

# Get plot from parameters
plot = Plot.get(
    plot_number=new_plot.plot_number,
    plot_column_number=new_plot.plot_column_number,
    plot_row_number=new_plot.plot_row_number,
    experiment_name=new_plot.experiment_name,
    season_name=new_plot.season_name,
    site_name=new_plot.site_name
)
print(f"Plot from parameters: {plot}")

# Add cultivar to plot
new_plot.add_cultivar(
    cultivar_accession=cultivar.cultivar_accession,
    cultivar_population=cultivar.cultivar_population
)
print(f"New Plot: {new_plot}")

# Get plot cultivars
cultivars = new_plot.get_cultivars()
print(f"Number of Cultivars: {len(cultivars)}")
for cultivar in cultivars:
    print(cultivar)

# Add plant to plot
new_plot.add_plant(
    plant_number=1,
    cultivar_accession=cultivar.cultivar_accession,
    cultivar_population=cultivar.cultivar_population,
    plant_info={"info": "info"}
)

# Get all plants
plants = new_plot.get_plants()
print(f"Number of Plants: {len(plants)}")
for plant in plants:
    print(plant)

# Update plot
new_plot.update(
    plot_number=100,
    plot_column_number=100,
    plot_row_number=100,
    plot_info={"info": "info"}
)
print(f"Updated Plot: {new_plot}")

# Delete plot
is_deleted = new_plot.delete()
print(f"Deleted Plot: {new_plot}")






# # Get all plots
# plots = Plot.get_all()
# plot_length = len(plots)
# print(f"Number of Plots: {plot_length}")

# # Select one plot
# plot = plots[0]
# print(f"Plot ID: {plot.id}")

# # Get Plot by ID
# plot = Plot.get_by_id(plot.id)
# print(f"Plot ID: {plot.id}")

# # Get Plot
# plot = Plot.get(
#     plot_number=plot.plot_number,
#     plot_column_number=plot.plot_column_number,
#     plot_row_number=plot.plot_row_number,
#     experiment_name=plot.experiment_name,
#     season_name=plot.season_name,
#     site_name=plot.site_name
# )
# print(f"Plot ID: {plot.id}")

# # Get Plot Valid Combos
# valid_combinations = Plot.get_valid_combinations()
# print(f"Number of Valid Combinations: {len(valid_combinations)}")

# # Get one of the valid combinations
# valid_combination = valid_combinations[0]
# print(f"Valid Combination: {valid_combination}")

# # Create a new plot
# new_plot = Plot.create(
#     plot_number=99,
#     plot_column_number=99,
#     plot_row_number=99,
#     experiment_name=valid_combination['experiment_name'],
#     season_name=valid_combination['season_name'],
#     site_name=valid_combination['site_name'],
#     cultivar_accession="Accession A1",
#     cultivar_population="Population A"
# )
# print(f"New Plot: {new_plot}")

# # Get plot cultivars
# cultivars = new_plot.get_cultivars()
# print(f"Number of Cultivars: {len(cultivars)}")
# for cultivar in cultivars:
#     print(cultivar)

# # Get plot plants
# plants = plot.get_plants()
# print(f"Number of Plants: {len(plants)}")
# for plant in plants:
#     print(plant)

# # Get another valid combination
# valid_combination = valid_combinations[-1]
# print(f"Valid Combination: {valid_combination}")

# # Set new plot experiment
# new_plot.set_experiment(experiment_name=valid_combination['experiment_name'])
# print(f"New Plot: {new_plot}")

# # Set new plot season
# new_plot.set_season(season_name=valid_combination['season_name'], experiment_name=valid_combination['experiment_name'])
# print(f"New Plot: {new_plot}")

# # Set new plot site
# new_plot.set_site(site_name=valid_combination['site_name'])
# print(f"New Plot: {new_plot}")

# # Create a new cultivar
# cultivar = new_plot.add_cultivar(
#     cultivar_accession="Accession A2",
#     cultivar_population="Population A"
# )
# print(f"New Cultivar: {cultivar}")

# # Create a new plant
# plant = new_plot.add_plant(
#     plant_number=1,
#     cultivar_accession="Accession A2",
#     cultivar_population="Population A",
#     plant_info={"info": "info"}
# )
# print(f"New Plant: {plant}")