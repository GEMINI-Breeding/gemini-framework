from gemini.api.plant import Plant
from gemini.api.cultivar import Cultivar

# Create a new Plant
new_plant = Plant.create(
    plant_number=4444,
    plant_info={
        "test": "test"
    }
)
print(f"Created New Plant: {new_plant}")

# Create a new Cultivar
new_cultivar = Cultivar.create(
    cultivar_population="Cultivar Test 1",
    cultivar_accession="Accession A",
    cultivar_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Cultivar: {new_cultivar}")

# Associate the plant with the cultivar
new_plant.associate_cultivar(
    cultivar_population="Cultivar Test 1",
    cultivar_accession="Accession A"
)
print(f"Associated Plant with Cultivar: {new_plant}")

# Check if the plant is associated with the cultivar
is_associated_cultivar = new_plant.belongs_to_cultivar(
    cultivar_population="Cultivar Test 1",
    cultivar_accession="Accession A"
)
print(f"Is Plant associated with Cultivar: {is_associated_cultivar}")

# Unassociate the plant from the cultivar
new_plant.unassociate_cultivar()
print(f"Unassociated Plant from Cultivar: {new_plant}")

# Check if the plant is unassociated from the cultivar
is_unassociated_cultivar = new_plant.belongs_to_cultivar(
    cultivar_population="Cultivar Test 1",
    cultivar_accession="Accession A"
)
print(f"Is Plant associated with cultivar: {is_unassociated_cultivar}")