from gemini.api.data_format import DataFormat
from gemini.api.data_type import DataType

# Get the Image Data Type
image_data_type = DataType.get("Image")
print(f"Image Data Type: {image_data_type}")

# Get associated data formats
associated_data_formats = image_data_type.get_associated_data_formats()
for data_format in associated_data_formats:
    print(f"Associated Data Format: {data_format}")

# Create a new data format
new_data_format = DataFormat.create(
    data_format_name="Test Image Format",
    data_format_mime_type="image/test",
    data_format_info={
        "description": "This is a test image format for API demonstration.",
        "version": "1.0",
    }
)
print(f"Created new data format: {new_data_format}")

# Associate the new data format with the image data type
image_data_type.associate_data_format(data_format_name=new_data_format.data_format_name)
print(f"Associated data type {image_data_type.data_type_name} with data format {new_data_format.data_format_name}")

# Check if the new data format is associated with the image data type
is_associated = image_data_type.belongs_to_data_format(data_format_name=new_data_format.data_format_name)
print(f"Is data format {new_data_format.data_format_name} associated with data type {image_data_type.data_type_name}? {is_associated}")

# Unassociate the new data format from the image data type
image_data_type.unassociate_data_format(data_format_name=new_data_format.data_format_name)
print(f"Unassociated data type {image_data_type.data_type_name} from data format {new_data_format.data_format_name}")

# Check if the unassociation was successful
is_associated_after_unassociation = image_data_type.belongs_to_data_format(data_format_name=new_data_format.data_format_name)
print(f"Is data format {new_data_format.data_format_name} still associated with data type {image_data_type.data_type_name}? {is_associated_after_unassociation}")

# Create a new data format for data type
new_data_format = image_data_type.add_new_data_format(
    data_format_name="New Test Image Format",
    data_format_mime_type="image/new_test",
    data_format_info={
        "description": "This is a new test image format for API demonstration.",
        "version": "1.1",
    }
)

print(f"Created new data format: {new_data_format}")
