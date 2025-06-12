from gemini.api.procedure import Procedure

# Get Procedure A
procedure_a = Procedure.get("Procedure A")
print(f"Got Procedure A: {procedure_a}")

# Create a new procedure run for Procedure A
new_procedure_a_run = procedure_a.create_new_run(
    procedure_run_info={"test": "test"}
)
print(f"Created New Procedure Run: {new_procedure_a_run}")

# Get Associated Procedure Runs
associated_procedure_runs = procedure_a.get_associated_runs()
for procedure_run in associated_procedure_runs:
    print(f"Associated Procedure Run: {procedure_run}")