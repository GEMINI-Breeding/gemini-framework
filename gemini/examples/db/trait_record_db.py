from gemini.db.models.columnar.trait_records import TraitRecordModel

filtered_records = TraitRecordModel.filter_records(
    experiment_names=["Experiment A", "Experiment B"],
)
print(f"Number of filtered records: {len(list(filtered_records))}")