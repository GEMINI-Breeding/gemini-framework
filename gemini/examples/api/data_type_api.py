from gemini.api.data_type import DataType

# Create a new data type
new_data_type = DataType.create(
    data_type_name="Data Type Test 1",
    data_type_info={"test": "test"},
)

# Get Data Type with data_type_name that does exist
data_type = DataType.get("Data Type Test 1")
print(f"Got Data Type: {data_type}")

# Get Data Type by ID
data_type = DataType.get_by_id(new_data_type.id)
print(f"Got Data Type by ID: {data_type}")

# Get all data types
all_data_types = DataType.get_all()
print(f"All Data Types:")
for data_type in all_data_types:
    print(data_type)

# Select first data type
first_data_type = all_data_types[0]

# Print all formats of the first data type
print(f"All Formats of the first Data Type:")
for data_format in first_data_type.get_formats():
    print(data_format)

# Search for data types
searched_data_types = DataType.search(data_type_name="Data Type Test 1")
length_searched_data_types = len(searched_data_types)
print(f"Found {length_searched_data_types} data types")

# Update the data type
data_type.update(
    data_type_info={"test": "test_updated"},
)
print(f"Updated Data Type: {data_type}")

# Refresh the data type
data_type.refresh()
print(f"Refreshed Data Type: {data_type}")

# Add a new format to the data type
new_data_format = new_data_type.create_format(
    data_format_name="Data Format Test K",
    data_format_mime_type="application/json",
    data_format_info={"test": "test"},
)

# Delete the new data type
is_deleted = new_data_type.delete()
print(f"Deleted Data Type: {is_deleted}")


