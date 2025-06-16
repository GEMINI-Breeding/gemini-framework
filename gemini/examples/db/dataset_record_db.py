from gemini.db.models.columnar.dataset_records import DatasetRecordModel

filtered_records = DatasetRecordModel.filter_records(
    experiment_names=["Experiment A", "Experiment B"],
)
print(f"Number of filtered records: {len(list(filtered_records))}")

