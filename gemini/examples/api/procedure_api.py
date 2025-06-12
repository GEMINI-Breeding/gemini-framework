from gemini.api.procedure import Procedure

# Create a new procedure
procedure = Procedure.create(
    procedure_name="Procedure Test 1",
    procedure_info={"test": "test"},
)
print(f"Created Procedure: {procedure}")

# Get Procedure with procedure_name
procedure = Procedure.get(
    procedure_name=procedure.procedure_name,
)
print(f"Got Procedure: {procedure}")

# Get Procedure by ID
procedure_by_id = Procedure.get_by_id(procedure.id)
print(f"Got Procedure by ID: {procedure_by_id}")

# Get all procedures
all_procedures = Procedure.get_all()
print(f"All Procedures:")
for proc in all_procedures:
    print(proc)

# Search for procedures
searched_procedures = Procedure.search(procedure_name="Procedure Test 1")
length_searched_procedures = len(searched_procedures)
print(f"Found {length_searched_procedures} procedures with procedure_name 'Procedure Test 1'")


# Refresh the procedure
procedure.refresh()
print(f"Refreshed Procedure: {procedure}")

# Update the procedure
procedure.update(
    procedure_info={"test": "test_updated"},
)
print(f"Updated Procedure: {procedure}")

# Set Procedure Info
procedure.set_info(
    procedure_info={"test": "test_set"},
)
print(f"Set Procedure Info: {procedure.get_info()}")

# Check if procedure exists before deletion
exists = Procedure.exists(
    procedure_name="Procedure Test 1",
)
print(f"Procedure exists: {exists}")

# Delete the created procedure
is_deleted = procedure.delete()
print(f"Deleted Procedure: {is_deleted}")

# Check if procedure exists after deletion
exists_after_deletion = Procedure.exists(
    procedure_name="Procedure Test 1",
)
print(f"Procedure exists after deletion: {exists_after_deletion}")
