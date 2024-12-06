from gemini.db.models.procedures import ProcedureModel

# Get all procedures
procedures = ProcedureModel.all()

# Print procedures
print("Procedures:")
for procedure in procedures:
    # Print Procedure
    print(f"{procedure.id}: {procedure.procedure_name}")
    # Print Runs
    for run in procedure.procedure_runs:
        print(f"Run: {run.id}")

    # Print Datasets
    for dataset in procedure.datasets:
        print(f"Dataset: {dataset.dataset_name}")