from gemini.api.procedure_run import ProcedureRun

# Create a new procedure run
new_procedure_run = ProcedureRun.create(
    procedure_run_info={"test": "test"}
)
print(f"Created Procedure Run: {new_procedure_run}")

# Get ProcedureRun with procedure_run_info
procedure_run = ProcedureRun.get(
    procedure_run_info=new_procedure_run.procedure_run_info
)
print(f"Got Procedure Run: {procedure_run}")

# Get ProcedureRun by ID
procedure_run_by_id = ProcedureRun.get_by_id(new_procedure_run.id)
print(f"Got Procedure Run by ID: {procedure_run_by_id}")

# Get all procedure runs
all_procedure_runs = ProcedureRun.get_all()
print(f"All Procedure Runs:")
for proc_run in all_procedure_runs[:10]:
    print(proc_run)

# Search for procedure runs
searched_procedure_runs = ProcedureRun.search(
    procedure_run_info={"test": "test"}
)
length_searched_procedure_runs = len(searched_procedure_runs)
print(f"Found {length_searched_procedure_runs} procedure runs with procedure_run_info 'test': 'test'")

# Refresh the procedure run
procedure_run.refresh()
print(f"Refreshed Procedure Run: {procedure_run}")

# Update the procedure run
procedure_run.update(
    procedure_run_info={"test": "test_updated"}
)
print(f"Updated Procedure Run: {procedure_run}")

# Set Procedure Run Info
procedure_run.set_info(
    procedure_run_info={"test": "test_set"}
)
print(f"Set Procedure Run Info: {procedure_run.get_info()}")

# Check if procedure run exists before deletion
exists = ProcedureRun.exists(
    procedure_run_info={"test": "test"}
)
print(f"Procedure Run exists: {exists}")

# Delete the created procedure run
is_deleted = new_procedure_run.delete()
print(f"Deleted Procedure Run: {is_deleted}")

# Check if procedure run exists after deletion
exists_after_deletion = ProcedureRun.exists(
    procedure_run_info={"test": "test"}
)
print(f"Procedure Run exists after deletion: {exists_after_deletion}")