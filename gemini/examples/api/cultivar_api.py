from gemini.api.cultivar import Cultivar

# Create a new cultivar with experiment Experiment A
new_cultivar = Cultivar.create(
    cultivar_population="Cultivar Test 1",
    cultivar_accession="Accession A",
    cultivar_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created Cultivar: {new_cultivar}")

# Check if created cultivar exists
exists = Cultivar.exists(
    cultivar_population="Cultivar Test 1",
    cultivar_accession="Accession A",
)
print(f"Cultivar exists: {exists}")

# Check a cultivar that does not exist
exists = Cultivar.exists(
    cultivar_population="Nonexistent Cultivar",
    cultivar_accession="Nonexistent Accession",
)
print(f"Nonexistent Cultivar exists: {exists}")

# Get Cultivar with cultivar_population and cultivar_accession that do exist
cultivar = Cultivar.get("Cultivar Test 1", "Accession A")
print(f"Got Cultivar: {cultivar}")

# Add to Experiment B
cultivar.assign_experiment("Experiment B")
print(f"Added Cultivar to Experiment B: {cultivar}")

# Check if it belongs to Experiment B
belongs = cultivar.belongs_to_experiment("Experiment B")
print(f"Belongs to Experiment B: {belongs}")

# Remove from Experiment B
cultivar.unassign_experiment("Experiment B")
print(f"Removed Cultivar from Experiment B: {cultivar}")

# Get Cultivar by ID
cultivar = Cultivar.get_by_id(new_cultivar.id)
print(f"Got Cultivar by ID: {cultivar}")

# Get all cultivars
all_cultivars = Cultivar.get_all()
print(f"All Cultivars:")
for cultivar in all_cultivars:
    print(cultivar)

# Search for cultivars
searched_cultivars = Cultivar.search(experiment_name="Experiment A")
length_searched_cultivars = len(searched_cultivars)
print(f"Found {length_searched_cultivars} cultivars in Experiment A")

# Refresh the cultivar
cultivar.refresh()
print(f"Refreshed Cultivar: {cultivar}")

# Update the cultivar
cultivar.update(
    cultivar_info={"test": "test_updated"},
)
print(f"Updated Cultivar: {cultivar}")

# Set Cultivar Info
cultivar.set_info(
    cultivar_info={"test": "test_set"},
)

# Get Cultivar Info
cultivar_info = cultivar.get_info()
print(f"Cultivar Info: {cultivar_info}")

# Delete the new cultivar
is_deleted = new_cultivar.delete()
print(f"Deleted Cultivar: {is_deleted}")