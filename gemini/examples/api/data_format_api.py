from gemini.api.data_format import DataFormat

# Create a new data format
new_data_format = DataFormat.create(
    data_format_name="Data Format Test 1",
    data_format_mime_type="application/json",
    data_format_info={"test": "test"},
)
print(f"Created Data Format: {new_data_format}")

# Check if created data format exists
exists = DataFormat.exists(
    data_format_name="Data Format Test 1",
)
print(f"Data Format exists: {exists}")

# Check a data format that does not exist
exists = DataFormat.exists(
    data_format_name="Nonexistent Data Format",
)
print(f"Nonexistent Data Format exists: {exists}")

# Get Data Format with data_format_name that does exist
data_format = DataFormat.get("Data Format Test 1")
print(f"Got Data Format: {data_format}")

# Get Data Format by ID
data_format = DataFormat.get_by_id(new_data_format.id)
print(f"Got Data Format by ID: {data_format}")

# Get all data formats
all_data_formats = DataFormat.get_all()
print(f"All Data Formats:")
for data_format in all_data_formats:
    print(data_format)

# Search for data formats
searched_data_formats = DataFormat.search(data_format_name="Data Format Test 1")
length_searched_data_formats = len(searched_data_formats)
print(f"Found {length_searched_data_formats} data formats")

# Update the data format
data_format.update(
    data_format_mime_type="text/csv",
    data_format_info={"test": "test_updated"},
)
print(f"Updated Data Format: {data_format}")

data_format.set_info(
    data_format_info={"test": "test_set"},
)
print(f"Set Data Format Info: {data_format}")

# Get Data Format Info
data_format_info = data_format.get_info()
print(f"Data Format Info: {data_format_info}")

# Refresh the data format
data_format = data_format.refresh()
print(f"Refreshed Data Format: {data_format}")

# Delete the data format
is_deleted = data_format.delete()
print(f"Deleted Data Format: {is_deleted}")
