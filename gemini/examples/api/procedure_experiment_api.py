from gemini.api.procedure import Procedure

# Create a new procedure for Experiment A
new_procedure = Procedure.create(
    procedure_name="Procedure Test 1",
    procedure_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Procedure: {new_procedure}")

# Get associated experiments
associated_experiments = new_procedure.get_associated_experiments()
for experiment in associated_experiments:
    print(f"Associated Experiment: {experiment}")

# Associate the procedure with Experiment B
new_procedure.associate_experiment(experiment_name="Experiment B")
print(f"Associated Procedure with Experiment B")

# Check if the procedure is associated with Experiment B
is_associated = new_procedure.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Procedure associated with Experiment B? {is_associated}")

# Unassociate the procedure from Experiment B
new_procedure.unassociate_experiment(experiment_name="Experiment B")
print(f"Unassociated Procedure from Experiment B")

# Verify the unassociation
is_associated_after_unassociation = new_procedure.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Procedure still associated with Experiment B? {is_associated_after_unassociation}")