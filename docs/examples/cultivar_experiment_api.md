# Cultivar Experiment API Example

This example demonstrates how to associate and unassociate cultivars with experiments using the Gemini framework.

## Source File Location

The original Python script is located at `gemini/examples/api/cultivar_experiment_api.py`.

## Code

```python
from gemini.api.cultivar import Cultivar

# Create a new cultivar for Experiment A
new_cultivar = Cultivar.create(
    cultivar_population="Cultivar Test 1",
    cultivar_accession="Accession A",
    cultivar_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created Cultivar: {new_cultivar}")

# Get Associated Experiments
associated_experiments = new_cultivar.get_associated_experiments()
for experiment in associated_experiments:
    print(f"Associated Experiment: {experiment}")

# Associate the cultivar with Experiment B
new_cultivar.associate_experiment(experiment_name="Experiment B")
print(f"Associated Cultivar with Experiment B")

# Check if the cultivar is associated with Experiment B
is_associated = new_cultivar.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Cultivar associated with Experiment B? {is_associated}")

# Unassociate the cultivar from Experiment B
new_cultivar.unassociate_experiment(experiment_name="Experiment B")
print(f"Unassociated Cultivar from Experiment B")

# Verify the unassociation
is_associated_after_unassociation = new_cultivar.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Cultivar still associated with Experiment B? {is_associated_after_unassociation}")
```

## Explanation

This example demonstrates how to manage the association between cultivars and experiments:

*   **Creating a cultivar:** A new cultivar is created and associated with Experiment A.
*   **Getting associated experiments:** The `get_associated_experiments()` method retrieves a list of experiments associated with the cultivar.
*   **Associating with an experiment:** The `associate_experiment()` method associates the cultivar with another experiment (Experiment B in this case).
*   **Checking association:** The `belongs_to_experiment()` method verifies if the cultivar is associated with a specific experiment.
*   **Unassociating from an experiment:** The `unassociate_experiment()` method removes the association between the cultivar and Experiment B.
*   **Verifying unassociation:** The `belongs_to_experiment()` method is used again to confirm that the cultivar is no longer associated with Experiment B.
