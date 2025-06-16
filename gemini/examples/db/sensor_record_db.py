from gemini.db.models.columnar.sensor_records import SensorRecordModel

filtered_records = SensorRecordModel.filter_records(
    experiment_names=["Experiment A", "Experiment B"],
)
print(f"Number of filtered records: {len(list(filtered_records))}")