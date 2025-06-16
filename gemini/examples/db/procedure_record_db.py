from gemini.db.models.columnar.procedure_records import ProcedureRecordModel

filtered_records = ProcedureRecordModel.filter_records(
    experiment_names=["Experiment A", "Experiment B"],
)
print(f"Number of filtered records: {len(list(filtered_records))}")