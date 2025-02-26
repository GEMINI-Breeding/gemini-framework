from gemini.api.plant import Plant
from gemini.api.plot import Plot

# Get all plants
plants = Plant.get_all()
print(f"All Plants:")
for plant in plants:
    print(plant)

# Get a single plant
plant = plants[0]
print(f"Single Plant: {plant}")

# Get Plant by ID
plant = Plant.get_by_id(plant.id)
print(f"Single Plant by ID: {plant}")

# Get Plant with plot_id and plant_number
plant = Plant.get(plant.plot_id, plant.plant_number)
print(f"Single Plant by plot_id and plant_number: {plant}")

# Search for plants
searched_plants = Plant.search(plot_id=plant.plot_id)
length_searched_plants = len(searched_plants)
print(f"Found {length_searched_plants} plants in plot_id {plant.plot_id}")

# Refresh the plant
plant = plant.refresh()
print(f"Refreshed Plant: {plant}")

# Create a new plant in the same plot
new_plant = Plant.create(
    plot_id=plant.plot_id,
    plant_number=6,
    cultivar_accession="Accession A1",
    cultivar_population="Population A",
    plant_info={"info": "info"}
)
print(f"New Plant: {new_plant}")

# Update the plant
new_plant.update(plant_info={"info": "updated info"})
print(f"Updated Plant: {new_plant}")

# Get Cultivar
cultivar = new_plant.get_cultivar()
print(f"Cultivar: {cultivar}")

# Set Cultivar
new_plant.set_cultivar(cultivar_accession="Accession A2", cultivar_population="Population A")
print(f"Updated Plant: {new_plant}")

# Delete the plant
is_deleted = new_plant.delete()
print(f"Deleted Plant: {is_deleted}")

