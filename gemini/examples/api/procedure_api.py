from gemini.api.procedure import Procedure
from gemini.api.experiment import Experiment

# Create a new procedure with an experiment name that does exist
new_procedure = Procedure.create(
    procedure_name="Procedure Test 1",
    procedure_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created Procedure: {new_procedure}")

# Get Procedure with procedure_name and experiment_name that do exist
procedure = Procedure.get("Procedure Test 1", "Experiment A")

# Get Procedure by ID
procedure = Procedure.get_by_id(new_procedure.id)

# Get all procedures
all_procedures = Procedure.get_all()
print(f"All Procedures:")
for procedure in all_procedures:
    print(procedure)

# Search for procedures
searched_procedures = Procedure.search(experiment_name="Experiment A")
length_searched_procedures = len(searched_procedures)
print(f"Found {length_searched_procedures} procedures in Experiment A")

# Refresh the procedure
procedure = procedure.refresh()
print(f"Refreshed Procedure: {procedure}")