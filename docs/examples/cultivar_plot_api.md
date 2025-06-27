# Cultivar Plot API Example

This example demonstrates how to associate and unassociate cultivars with plots using the Gemini framework.

## Source File Location

The original Python script is located at `gemini/examples/api/cultivar_plot_api.py`.

## Code

```python
from gemini.api.plot import Plot
from gemini.api.cultivar import Cultivar

# Create a plot object
new_plot = Plot.create(
    plot_number=100,
    plot_row_number=101,
    plot_column_number=101,
    plot_info={
        "plot_type": "test",
        "plot_size": 100,
        "plot_location": "test_location",
    },
    experiment_name="Experiment A",
    season_name="Season 1A",
    site_name="Site A1"
)
print(f"Plot created: {new_plot}")

# Create a new cultivar for Experiment A
new_cultivar = Cultivar.create(
    cultivar_accession="Test Cultivar",
    cultivar_population="Test Population",
    experiment_name="Experiment A",
    cultivar_info={
        "cultivar_type": "test",
        "cultivar_size": 100,
        "cultivar_location": "test_location",
    }
)
print(f"Cultivar created: {new_cultivar}")

# Associate the plot with the cultivar
new_cultivar.associate_plot(
    plot_number=new_plot.plot_number,
    plot_row_number=new_plot.plot_row_number,
    plot_column_number=new_plot.plot_column_number,
    experiment_name=new_plot.experiment_name,
    season_name=new_plot.season_name,
    site_name=new_plot.site_name
)
print(f"Plot {new_plot.plot_number} associated with Cultivar {new_cultivar.cultivar_accession}")

# Get all the plots associated with the cultivar
associated_plots = new_cultivar.get_associated_plots()
for plot in associated_plots:
    print(f"Associated Plot: {plot.plot_number}, Row: {plot.plot_row_number}, Column: {plot.plot_column_number}")

# Check association of plot with cultivar
is_associated = new_cultivar.belongs_to_plot(
    plot_number=new_plot.plot_number,
    plot_row_number=new_plot.plot_row_number,
    plot_column_number=new_plot.plot_column_number,
    experiment_name=new_plot.experiment_name,
    season_name=new_plot.season_name,
    site_name=new_plot.site_name
)
print(f"Is Plot {new_plot.plot_number} associated with Cultivar {new_cultivar.cultivar_accession}? {is_associated}")

# Remove the association
new_cultivar.unassociate_plot(
    plot_number=new_plot.plot_number,
    plot_row_number=new_plot.plot_row_number,
    plot_column_number=new_plot.plot_column_number,
    experiment_name=new_plot.experiment_name,
    season_name=new_plot.season_name,
    site_name=new_plot.site_name
)
print(f"Plot {new_plot.plot_number} unassociated from Cultivar {new_cultivar.cultivar_accession}")

# Check if the plot is still associated
is_associated = new_cultivar.belongs_to_plot(
    plot_number=new_plot.plot_number,
    plot_row_number=new_plot.plot_row_number,
    plot_column_number=new_plot.plot_column_number,
    experiment_name=new_plot.experiment_name,
    season_name=new_plot.season_name,
    site_name=new_plot.site_name
)
print(f"Is Plot {new_plot.plot_number} associated with Cultivar {new_cultivar.cultivar_accession}? {is_associated}")
```

## Explanation

This example demonstrates how to manage the association between cultivars and plots:

*   **Creating a plot:** A new plot is created with specific attributes like plot number, row number, and column number.
*   **Creating a cultivar:** A new cultivar is created and associated with Experiment A.
*   **Associating with a plot:** The `associate_plot()` method associates the cultivar with the created plot.
*   **Getting associated plots:** The `get_associated_plots()` method retrieves a list of plots associated with the cultivar.
*   **Checking association:** The `belongs_to_plot()` method verifies if the cultivar is associated with a specific plot.
*   **Unassociating from a plot:** The `unassociate_plot()` method removes the association between the cultivar and the plot.
*   **Verifying unassociation:** The `belongs_to_plot()` method is used again to confirm that the cultivar is no longer associated with the plot.
