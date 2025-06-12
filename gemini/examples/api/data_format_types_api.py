from gemini.api.data_format import DataFormat
from gemini.api.data_type import DataType 

# Get the PNG data format
png_format = DataFormat.get("PNG")
print(f"PNG Data Format: {png_format}")

# Get associated data types
associated_data_types = png_format.get_associated_data_types()
for data_type in associated_data_types:
    print(f"Associated Data Type: {data_type}")

# Create a new data type
new_data_type = DataType.create(
    data_type_name="Test Data Type",
    data_type_info={
        "description": "This is a test data type for API demonstration.",
        "version": "1.0",
    }
)
print(f"Created new data type: {new_data_type}")

# Associate the new data type with the PNG data format
png_format.associate_data_type(data_type_name=new_data_type.data_type_name)
print(f"Associated data format {png_format.data_format_name} with data type {new_data_type.data_type_name}")

# Check if Belongs to Data Type
is_associated = png_format.belongs_to_data_type(data_type_name=new_data_type.data_type_name)
print(f"Is data format {png_format.data_format_name} associated with data type {new_data_type.data_type_name}? {is_associated}")

# Unassociate the data format from the data type
png_format.unassociate_data_type(data_type_name=new_data_type.data_type_name)
print(f"Unassociated data format {png_format.data_format_name} from data type {new_data_type.data_type_name}")

# Verify the unassociation
is_associated_after_unassociation = png_format.belongs_to_data_type(data_type_name=new_data_type.data_type_name)
print(f"Is data format {png_format.data_format_name} still associated with data type {new_data_type.data_type_name}? {is_associated_after_unassociation}")