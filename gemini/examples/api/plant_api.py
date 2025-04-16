from gemini.api.cultivar import Cultivar
from gemini.api.plant import Plant
from gemini.api.plot import Plot

all_plots = Plot.get_all()
print(f"Number of Plots: {len(all_plots)}")
single_plot = all_plots[0]
print(f"Plot ID: {single_plot.id}")

all_cultivars = Cultivar.get_all()
print(f"Number of Cultivars: {len(all_cultivars)}")
single_cultivar = all_cultivars[0]
print(f"Cultivar ID: {single_cultivar.id}")

# Create a new plant
new_plant = Plant.create(
    plot_id=single_plot.id,
    plant_number=1000,
    cultivar_accession=single_cultivar.cultivar_accession,
    cultivar_population=single_cultivar.cultivar_population,
    plant_info={"info": "info"}
)
print(f"New Plant: {new_plant}")

# Get plant from ID
plant = Plant.get_by_id(new_plant.id)
print(f"Plant from ID: {plant}")

# Get plant from parameters
plant = Plant.get(
    plot_id=new_plant.plot_id,
    plant_number=new_plant.plant_number
)
print(f"Plant from parameters: {plant}")

# Get all plants
plants = Plant.get_all()
print(f"Number of Plants: {len(plants)}")
for plant in plants:
    print(plant)

# Update plant
plant.update(
    plant_number=2000,
    plant_info={"info": "info_updated"}
)
print(f"Updated Plant: {plant}")

# Set Plant Info
plant.set_info(
    plant_info={"info": "info_set"}
)
print(f"Set Plant Info: {plant}")

# Get Plant Info
plant_info = plant.get_info()
print(f"Plant Info: {plant_info}")

# Refresh plant
plant.refresh()
print(f"Refreshed Plant: {plant}")

# Search for plants
searched_plants = Plant.search(cultivar_accession=single_cultivar.cultivar_accession)
length_searched_plants = len(searched_plants)
print(f"Found {length_searched_plants} plants with cultivar accession {single_cultivar.cultivar_accession}")

# Alternative Cultivar
alt_cultivar = all_cultivars[-1]
print(f"Alternative Cultivar ID: {alt_cultivar.id}")

# Set cultivar to alternative cultivar
new_plant.set_cultivar(
    cultivar_accession=alt_cultivar.cultivar_accession,
    cultivar_population=alt_cultivar.cultivar_population
)
print(f"Updated Plant with Alternative Cultivar: {new_plant}")

# Get the cultivar
cultivar = new_plant.get_cultivar()
print(f"Cultivar: {cultivar}")

# Delete plant
is_deleted = plant.delete()
print(f"Deleted Plant: {is_deleted}")
