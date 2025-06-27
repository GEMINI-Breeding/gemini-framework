# Plot Cultivar API Example

This example demonstrates how to associate and unassociate cultivars with plots using the Gemini framework.

## Source File Location

The original Python script is located at `gemini/examples/api/plot_cultivar_api.py`.

## Code

```python
from gemini.api.plot import Plot
from gemini.api.cultivar import Cultivar

try:
    # Create a new Plot for Experiment A
    new_plot = Plot.create(
        plot_number=2000,
        plot_row_number=101,
        plot_column_number=101,
        experiment_name="Experiment A",
        season_name="Season 1A",
        site_name="Site A1",
        plot_info={"test": "test"},
    )
    print(f"Created Plot: {new_plot}")

    # Create a new Cultivar for Experiment A
    new_cultivar = Cultivar.create(
        cultivar_population="Cultivar Test 1",
        cultivar_accession="Accession A",
        cultivar_info={"test": "test"},
        experiment_name="Experiment A"
    )
    print(f"Created Cultivar: {new_cultivar}")

    # Associate the plot with the cultivar
    new_plot.associate_cultivar(
        cultivar_population="Cultivar Test 1",
        cultivar_accession="Accession A"
    )
    print(f"Associated Plot with Cultivar: {new_plot}")

    # Check if the plot is associated with the cultivar
    is_associated_cultivar = new_plot.belongs_to_cultivar(
        cultivar_population="Cultivar Test 1",
        cultivar_accession="Accession A"
    )
    print(f"Is Plot associated with Cultivar: {is_associated_cultivar}")

    # Unassociate the plot from the cultivar
    new_plot.unassociate_cultivar(
        cultivar_population="Cultivar Test 1",
        cultivar_accession="Accession A"
    )
    print(f"Unassociated Plot from Cultivar: {new_plot}")

    # Check if the plot is unassociated from the cultivar
    is_unassociated_cultivar = new_plot.belongs_to_cultivar(
        cultivar_population="Cultivar Test 1",
        cultivar_accession="Accession A"
    )
    print(f"Is Plot unassociated from Cultivar: {is_unassociated_cultivar}")
    

finally:
    # Clean up: Delete the created plot and cultivar
    if new_plot:
        new_plot.delete()
        print(f"Deleted Plot: {new_plot}")

    if new_cultivar:
        new_cultivar.delete()
        print(f"Deleted Cultivar: {new_cultivar}")
```

## Explanation

This example demonstrates how to manage the association between cultivars and plots:

*   **Creating a plot:** The `Plot.create()` method is used to create a new plot with plot information, additional information, and associated experiment, season, and site.
*   **Creating a cultivar:** The `Cultivar.create()` method is used to create a new cultivar with a population, accession, additional information, and associated experiment.
*   **Associating with a cultivar:** The `associate_cultivar()` method associates the plot with the created cultivar.
*   **Checking association:** The `belongs_to_cultivar()` method verifies if the plot is associated with a specific cultivar.
*   **Unassociating from a cultivar:** The `unassociate_cultivar()` method removes the association between the plot and the cultivar.
*   **Verifying unassociation:** The `belongs_to_cultivar()` method is used again to confirm that the plot is no longer associated with the cultivar.
*   **Cleaning up:** The `delete()` method is used to delete the created plot and cultivar.
