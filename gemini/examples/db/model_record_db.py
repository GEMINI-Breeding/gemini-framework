from gemini.db.models.columnar.model_records import ModelRecordModel

filtered_records = ModelRecordModel.filter_records(

)
print(f"Number of filtered records: {len(list(filtered_records))}")