from gemini.db.models.cultivars import CultivarModel

# Get all cultivars
cultivars = CultivarModel.all()

# Get cultivar by id
cultivar = CultivarModel.get(1)

# Get cultivar by parameters
cultivar = CultivarModel.get_by_parameters(
    cultivar_population="Default",
    cultivar_accession="Default"
)

