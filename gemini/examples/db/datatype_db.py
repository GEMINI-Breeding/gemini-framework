from gemini.db.models.data_types import DataTypeModel

# Get all data types
data_types = DataTypeModel.all()

# Print data types
print("Data Types:")
for data_type in data_types:
    format_list = [f.data_format_name for f in data_type.formats]
    print(f"{data_type.id}: {data_type.data_type_name} {format_list}")