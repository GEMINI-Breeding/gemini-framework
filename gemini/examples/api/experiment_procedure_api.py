from gemini.api.experiment import Experiment
from gemini.api.procedure import Procedure

# Create a new procedure for Experiment A
new_procedure = Procedure.create(
    procedure_name="New Procedure",
    procedure_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Procedure: {new_procedure}")

# Get Experiment B
experiment_b = Experiment.get("Experiment B")
print(f"Got Experiment B: {experiment_b}")

# Associate Experiment B with the new procedure
experiment_b.associate_procedure(procedure_name=new_procedure.procedure_name)
print(f"Associated New Procedure with Experiment B: {experiment_b}")

# Get Associated Procedures
associated_procedures = experiment_b.get_associated_procedures()
for procedure in associated_procedures:
    print(f"Associated Procedure: {procedure}")

# Check if the new procedure is associated with Experiment B
is_associated = experiment_b.belongs_to_procedure(procedure_name=new_procedure.procedure_name)
print(f"Is New Procedure associated with Experiment B? {is_associated}")

# Unassociate the new procedure from Experiment B
experiment_b.unassociate_procedure(procedure_name=new_procedure.procedure_name)
print(f"Unassociated New Procedure from Experiment B: {experiment_b}")

# Check if the new procedure is still associated with Experiment B
is_associated = experiment_b.belongs_to_procedure(procedure_name=new_procedure.procedure_name)
print(f"Is New Procedure still associated with Experiment B? {is_associated}")

# Create a new procedure for Experiment B
experiment_procedure = experiment_b.create_new_procedure(
    procedure_name="Experiment B Procedure",
    procedure_info={"test": "test"}
)
print(f"Created New Procedure: {experiment_procedure}")