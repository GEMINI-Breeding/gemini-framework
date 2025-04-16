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

# Update the procedure
procedure.update(
    procedure_info={"test": "test_updated"},
)

# Set Procedure Info
procedure.set_info(
    procedure_info={"test": "test_set"},
)

# Get Procedure Info
procedure_info = procedure.get_info()
print(f"Procedure Info: {procedure_info}")

# Create 10 new procedure runs
for i in range(10):
    procedure.create_run(
        procedure_run_info={
            "test_info": f"test_value_{i}"
        }
    )
    print(f"Created Procedure Run {i + 1}")

# Get all runs for the procedure
procedure_runs = procedure.get_runs()
print(f"All Procedure Runs:")
for procedure_run in procedure_runs:
    print(procedure_run)

# Create a dataset for the procedure
dataset = procedure.create_dataset(
    dataset_name="Dataset Test 1",
    dataset_info={"test": "test"},
    collection_date="2023-10-01",
    experiment_name="Experiment A",
)
print(f"Created Dataset: {dataset}")

# Get all datasets for the procedure
procedure_datasets = procedure.get_datasets()
print(f"All Procedure Datasets:")
for procedure_dataset in procedure_datasets:
    print(procedure_dataset)

# Delete the procedure
is_deleted = procedure.delete()
print(f"Deleted Procedure: {is_deleted}")