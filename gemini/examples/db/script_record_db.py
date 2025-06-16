from gemini.db.models.columnar.script_records import ScriptRecordModel

filtered_records = ScriptRecordModel.filter_records(
    experiment_names=["Experiment A", "Experiment B"],
)
print(f"Number of filtered records: {len(list(filtered_records))}")