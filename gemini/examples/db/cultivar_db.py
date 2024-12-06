from gemini.db.models.cultivars import CultivarModel


# Get all cultivars
cultivars = CultivarModel.all()

# Print cultivars
print("Cultivars:")
for cultivar in cultivars:
    print(f"{cultivar.id}: {cultivar.cultivar_accession} {cultivar.cultivar_population}")