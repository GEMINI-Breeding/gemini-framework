from gemini.api.experiment import Experiment
from gemini.api.plot import Plot

# Create a new plot for Experiment A
new_plot = Plot.create(
    plot_number=1000,
    plot_row_number=1001,
    plot_column_number=1001,
    experiment_name="Experiment A",
    season_name="Season 1A",
    site_name="Site A1"
)
print(f"Created New Plot: {new_plot}")

# Get Experiment B
experiment_b = Experiment.get("Experiment B")
print(f"Got Experiment B: {experiment_b}")

# Associate Experiment B with the new plot
experiment_b.associate_plot(
    plot_number=new_plot.plot_number,
    plot_row_number=new_plot.plot_row_number,
    plot_column_number=new_plot.plot_column_number,
    season_name=new_plot.season_name,
    site_name=new_plot.site_name
)
print(f"Associated New Plot with Experiment B: {experiment_b}")

# Get Associated Plots
associated_plots = experiment_b.get_associated_plots()
for plot in associated_plots:
    print(f"Associated Plot: {plot}")

# Check if the new plot is associated with Experiment B
is_associated = experiment_b.belongs_to_plot(
    plot_number=new_plot.plot_number,
    plot_row_number=new_plot.plot_row_number,
    plot_column_number=new_plot.plot_column_number,
    season_name=new_plot.season_name,
    site_name=new_plot.site_name
)
print(f"Is New Plot associated with Experiment B? {is_associated}")

# Unassociate the new plot from Experiment B
experiment_b.unassociate_plot(
    plot_number=new_plot.plot_number,
    plot_row_number=new_plot.plot_row_number,
    plot_column_number=new_plot.plot_column_number,
    season_name=new_plot.season_name,
    site_name=new_plot.site_name
)
print(f"Unassociated New Plot from Experiment B: {experiment_b}")

# Check if the new plot is still associated with Experiment B
is_associated = experiment_b.belongs_to_plot(
    plot_number=new_plot.plot_number,
    plot_row_number=new_plot.plot_row_number,
    plot_column_number=new_plot.plot_column_number,
    season_name=new_plot.season_name,
    site_name=new_plot.site_name
)
print(f"Is New Plot still associated with Experiment B? {is_associated}")

# Create a new plot for Experiment B
experiment_plot = experiment_b.create_new_plot(
    plot_number=2000,
    plot_row_number=2001,
    plot_column_number=2001,
    season_name="Season 2B",
    site_name="Site B2"
)
print(f"Created New Plot: {experiment_plot}")