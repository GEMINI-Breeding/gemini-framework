from gemini.api.plot import Plot
from gemini.api.site import Site

try:
    # Create a new Plot for Experiment A
    new_plot = Plot.create(
        plot_number=1000,
        plot_row_number=101,
        plot_column_number=101,
        experiment_name="Experiment A",
        season_name="Season 1A",
        site_name="Site A1",
        plot_info={"test": "test"},
    )
    print(f"Created Plot: {new_plot}")

    # Get current Experiment
    current_site = new_plot.get_associated_site()
    print(f"Current Site: {current_site}")

    # Create a new Site for Experiment A called Site X
    new_site = Site.create(
        site_name="Site X",
        site_info={"test": "test"},
        experiment_name="Experiment A",
    )
    print(f"Created New Site: {new_site}")

    # For the new plot, associate it with the new site
    new_plot.associate_site(site_name="Site X")

    # Check if the plot is associated with the new site
    is_associated_site = new_plot.belongs_to_site("Site X")
    print(f"Is Plot associated with Site X: {is_associated_site}")

    # Now unassociate the plot from the new site
    new_plot.unassociate_site()
    # Check if the plot is unassociated from the new site
    is_unassociated_site = new_plot.belongs_to_site("Site X")
    print(f"Is Plot unassociated from Site X: {is_unassociated_site}")

finally:
    # Clean up: Delete the created plot and site
    if new_plot:
        new_plot.delete()
        print(f"Deleted Plot: {new_plot}")

    if new_site:
        new_site.delete()
        print(f"Deleted Site: {new_site}")

