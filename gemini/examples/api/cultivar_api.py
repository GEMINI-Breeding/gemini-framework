from gemini.api.cultivar import Cultivar

# Create a new Cultivar for Experiment A
new_cultivar = Cultivar.create(
    cultivar_population="Cultivar Test 1",
    cultivar_accession="Accession A",
    cultivar_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created Cultivar: {new_cultivar}")

# Get Cultivar with Population and Accession
cultivar = Cultivar.get("Cultivar Test 1", "Accession A")
print(f"Got Cultivar: {cultivar}")

# Get the same Cultivar by ID
cultivar_by_id = Cultivar.get_by_id(new_cultivar.id)
print(f"Got Cultivar by ID: {cultivar_by_id}")

# Get all cultivars
all_cultivars = Cultivar.get_all()
print(f"All Cultivars:")
for cultivar in all_cultivars:
    print(cultivar)

# Search for cultivars in Experiment A
searched_cultivars = Cultivar.search(experiment_name="Experiment A")
length_searched_cultivars = len(searched_cultivars)
print(f"Found {length_searched_cultivars} cultivars in Experiment A")

# Refresh the cultivar
cultivar.refresh()
print(f"Refreshed Cultivar: {cultivar}")

# Update the cultivar_info
cultivar.set_info(
    cultivar_info={"test": "test_updated"},
)
print(f"Updated Cultivar Info: {cultivar.get_info()}")

# Check if the cultivar exists before deletion
exists = Cultivar.exists(
    cultivar_population="Cultivar Test 1",
    cultivar_accession="Accession A"
)
print(f"Cultivar exists: {exists}")

# Delete the created cultivar
is_deleted = new_cultivar.delete()
print(f"Deleted Cultivar: {is_deleted}")

# Check if the cultivar exists after deletion
exists_after_deletion = Cultivar.exists(
    cultivar_population="Cultivar Test 1",
    cultivar_accession="Accession A"
)
print(f"Cultivar exists after deletion: {exists_after_deletion}")
