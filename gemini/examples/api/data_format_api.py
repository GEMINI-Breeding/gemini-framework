from gemini.api.data_format import DataFormat

# Create a new data format
new_data_format = DataFormat.create(
    data_format_name="Test Data Format",
    data_format_mime_type="application/json",
    data_format_info={
        "format_type": "test",
        "format_size": 100,
        "format_location": "test_location",
    }
)
print(f"Data Format created: {new_data_format}")

# Get Data Format by ID
data_format_by_id = DataFormat.get_by_id(new_data_format.id)
print(f"Data Format by ID: {data_format_by_id}")

# Get Data Format by Name
data_format_by_name = DataFormat.get(data_format_name="Test Data Format")
print(f"Data Format by Name: {data_format_by_name}")

# Get all Data Formats
all_data_formats = DataFormat.get_all()
for data_format in all_data_formats:
    print(data_format)

# Search Data Formats
search_results = DataFormat.search(data_format_name="Test Data Format")
for result in search_results:
    print(f"Search Result: {result}")

# Update Data Format
data_format = data_format.update(
    data_format_mime_type="application/xml",
    data_format_info={
        "format_type": "updated_test",
        "format_size": 200,
        "format_location": "updated_test_location",
    },
)
print(f"Updated Data Format: {data_format}")

# Set Data Format Info
data_format.set_info(
    data_format_info={
        "format_type": "new_test",
        "format_size": 300,
        "format_location": "new_test_location",
    }
)
print(f"Data Format Info set: {data_format.get_info()}")

# Check if Data Format exists
data_format_exists = DataFormat.exists(data_format_name="Test Data Format")
print(f"Does Data Format exist? {data_format_exists}")

# Delete Data Format
data_format.delete()
print(f"Data Format deleted: {data_format}")

# Check if Data Format exists after deletion
data_format_exists_after_deletion = DataFormat.exists(data_format_name="Test Data Format")
print(f"Does Data Format exist after deletion? {data_format_exists_after_deletion}")