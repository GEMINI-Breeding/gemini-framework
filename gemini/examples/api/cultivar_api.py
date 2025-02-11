from gemini.api.cultivar import Cultivar

all_cultivars = Cultivar.get_all()
for cultivar in all_cultivars:
    print(cultivar)

cultivar_accessions = Cultivar.get_population_accessions("Population A")
for accession in cultivar_accessions:
    print(accession)
