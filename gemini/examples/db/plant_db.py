from gemini.db.models.plants import PlantModel

# Get All Plants
plants = PlantModel.all()

# Print Plants
print("Plants:")
for plant in plants:
    print(f"{plant.id}: {plant.plant_number}")

    # Print Cultivar
    print(f"Cultivar: {plant.cultivar.cultivar_accession} {plant.cultivar.cultivar_population}")


