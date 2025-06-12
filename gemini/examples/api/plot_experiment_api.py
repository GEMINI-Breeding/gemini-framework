from gemini.api.plot import Plot
from gemini.api.experiment import Experiment

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
    current_experiment = new_plot.get_associated_experiment()
    print(f"Current Experiment: {current_experiment}")

    # Get current Season
    current_season = new_plot.get_associated_season()
    print(f"Current Season: {current_season}")

    # Create a new experiment Experiment X
    new_experiment = Experiment.create(
        experiment_name="Experiment X",
        experiment_info={"test": "test"},
        experiment_end_date="2024-12-31",
        experiment_start_date="2024-01-01",
    )
    print(f"Created New Experiment: {new_experiment}")

    # For this experiment create a new season
    new_season = new_experiment.create_new_season(
        season_name="Season X",
        season_info={"test": "test"},
        season_start_date="2024-01-01",
        season_end_date="2024-12-31",
    )
    print(f"Created New Season: {new_season}")

    # For the new plot, associate it with the new experiment and season
    new_plot.associate_experiment(experiment_name="Experiment X")
    new_plot.associate_season(season_name="Season X", experiment_name="Experiment X")
    
    # Check if the plot is associated with the new experiment and season
    is_associated_experiment = new_plot.belongs_to_experiment("Experiment X")
    is_associated_season = new_plot.belongs_to_season("Season X", "Experiment X")

    print(f"Is Plot associated with Experiment X: {is_associated_experiment}")
    print(f"Is Plot associated with Season X: {is_associated_season}")

    # Now unassociate the plot from the new experiment and season
    new_plot.unassociate_experiment()
    new_plot.unassociate_season()

    # Check if the plot is unassociated from the new experiment and season
    is_unassociated_experiment = new_plot.belongs_to_experiment("Experiment X")
    is_unassociated_season = new_plot.belongs_to_season("Season X", "Experiment X")
    print(f"Is Plot unassociated from Experiment X: {is_unassociated_experiment}")
    print(f"Is Plot unassociated from Season X: {is_unassociated_season}")

finally:
    delete_plot = new_plot.delete()
    print(f"Deleted Plot: {delete_plot}")

