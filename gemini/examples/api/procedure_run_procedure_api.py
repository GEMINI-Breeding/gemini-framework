from gemini.api.procedure import Procedure
from gemini.api.procedure_run import ProcedureRun

# Create a new procedure run for Procedure A
new_procedure_run = ProcedureRun.create(
    procedure_run_info={"test": "test"},
    procedure_name="Procedure A"
)
print(f"Created New Procedure Run: {new_procedure_run}")

# Create a new procedure for Experiment A
new_procedure = Procedure.create(
    procedure_name="Procedure X",
    procedure_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Procedure: {new_procedure}")

# Get associated procedure of the new procedure run
associated_procedure = new_procedure_run.get_associated_procedure()
print(f"Associated Procedure: {associated_procedure}")

# Associate the new procedure run with the new procedure
new_procedure_run.associate_procedure(procedure_name=new_procedure.procedure_name)
print(f"Associated New Procedure Run with New Procedure: {new_procedure_run}")

# Check if the new procedure run is associated with the new procedure
is_associated = new_procedure_run.belongs_to_procedure(procedure_name=new_procedure.procedure_name)
print(f"Is New Procedure Run associated with New Procedure? {is_associated}")

# Unassociate the new procedure run from the new procedure
new_procedure_run.unassociate_procedure()
print(f"Unassociated New Procedure Run from New Procedure: {new_procedure_run}")

# Check if the new procedure run is still associated with the new procedure
is_associated = new_procedure_run.belongs_to_procedure(procedure_name=new_procedure.procedure_name)
print(f"Is New Procedure Run still associated with New Procedure? {is_associated}")