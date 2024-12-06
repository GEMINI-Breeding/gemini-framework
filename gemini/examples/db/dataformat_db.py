from gemini.db.models.data_formats import DataFormatModel

# Get All Data Formats
data_formats = DataFormatModel.all()

# Print Data Formats
print("Data Formats:")
for data_format in data_formats:
    print(f"{data_format.id}: {data_format.data_format_name}")