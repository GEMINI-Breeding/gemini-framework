from gemini.api.procedure import Procedure
from gemini.api.procedure_run import ProcedureRun

# Get procedure by name
procedure = Procedure.get("Procedure A")
print(f"Got Procedure: {procedure}")

# Create a new procedure run
procedure_run = ProcedureRun.create(
    procedure_run_info={"test": "test"},
    procedure_name=procedure.procedure_name
)
print(f"Created Procedure Run: {procedure_run}")

# Get ProcedureRun with procedure_run_info that does exist
procedure_run = ProcedureRun.get({"test": "test"}, procedure_name=procedure.procedure_name)
print(f"Got ProcedureRun: {procedure_run}")

# Get ProcedureRun by ID
procedure_run = ProcedureRun.get_by_id(procedure_run.id)
print(f"Got ProcedureRun by ID: {procedure_run}")

# Get all procedure runs
all_procedure_runs = ProcedureRun.get_all()
print(f"All Procedure Runs:")
for procedure_run in all_procedure_runs:
    print(procedure_run)

# Search for procedure runs
searched_procedure_runs = ProcedureRun.search(procedure_name=procedure.procedure_name)
length_searched_procedure_runs = len(searched_procedure_runs)
print(f"Found {length_searched_procedure_runs} procedure runs")

# Refresh the procedure run
procedure_run.refresh()
print(f"Refreshed Procedure Run: {procedure_run}")

# Update the procedure run
procedure_run.update(
    procedure_run_info={"test": "test_updated"},
)
print(f"Updated Procedure Run: {procedure_run}")

# Delete the procedure run
is_deleted = procedure_run.delete()
print(f"Deleted Procedure Run: {is_deleted}")