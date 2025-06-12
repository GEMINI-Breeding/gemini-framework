from gemini.api.site import Site
from gemini.api.experiment import Experiment
from gemini.api.plot import Plot

# Create a new Plot for Experiment A and Site A1
new_plot = Plot.create(
    plot_number=1011,
    plot_row_number=1011,
    plot_column_number=1011,
    experiment_name="Experiment A",
    season_name="Season 1A",
    site_name="Site A1"
)
print(f"Created New Plot: {new_plot}")

# Get Site A2
site_a2 = Site.get("Site A2")
print(f"Got Site A2: {site_a2}")

# Create a new plot for Site A2 explicitly
site_a2.create_new_plot(
    plot_number=2022,
    plot_row_number=2022,
    plot_column_number=2022,
    season_name="Season 1A",
    experiment_name="Experiment A"
)

# Associate Site A2 with the new plot
site_a2.associate_plot(
    plot_number=new_plot.plot_number,
    plot_row_number=new_plot.plot_row_number,
    plot_column_number=new_plot.plot_column_number,
    season_name=new_plot.season_name,
    experiment_name=new_plot.experiment_name
)
print(f"Associated New Plot with Site A2: {site_a2}")

# Get Associated Plots
associated_plots = site_a2.get_associated_plots()
for plot in associated_plots:
    print(f"Associated Plot: {plot}")

# Check if the new plot is associated with Site A2
is_associated = site_a2.belongs_to_plot(
    plot_number=new_plot.plot_number,
    plot_row_number=new_plot.plot_row_number,
    plot_column_number=new_plot.plot_column_number,
    season_name=new_plot.season_name,
    experiment_name=new_plot.experiment_name
)
print(f"Is New Plot associated with Site A2? {is_associated}")

# Unassociate the new plot from Site A2
site_a2.unassociate_plot(
    plot_number=new_plot.plot_number,
    plot_row_number=new_plot.plot_row_number,
    plot_column_number=new_plot.plot_column_number,
    season_name=new_plot.season_name,
    experiment_name=new_plot.experiment_name
)
print(f"Unassociated New Plot from Site A2: {site_a2}")

# Check if the new plot is still associated with Site A2
is_associated = site_a2.belongs_to_plot(
    plot_number=new_plot.plot_number,
    plot_row_number=new_plot.plot_row_number,
    plot_column_number=new_plot.plot_column_number,
    season_name=new_plot.season_name,
    experiment_name=new_plot.experiment_name
)
print(f"Is New Plot still associated with Site A2? {is_associated}")
