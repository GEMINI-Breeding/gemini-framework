from gemini.api.experiment import Experiment
from gemini.api.cultivar import Cultivar

# Create a new cultivar for Experiment A
new_cultivar = Cultivar.create(
    cultivar_accession="New Cultivar",
    cultivar_population="New Population",
    cultivar_info={"test": "test"},
    experiment_name="Experiment A"
)

# Get Experiment B
experiment_b = Experiment.get("Experiment B")
print(f"Got Experiment B: {experiment_b}")

# Associate Experiment B with the new cultivar
experiment_b.associate_cultivar(
    cultivar_accession=new_cultivar.cultivar_accession,
    cultivar_population=new_cultivar.cultivar_population
)

# Get Associated Cultivars
associated_cultivars = experiment_b.get_associated_cultivars()
for cultivar in associated_cultivars:
    print(f"Associated Cultivar: {cultivar}")

# Check if the new cultivar is associated with Experiment B
is_associated = experiment_b.belongs_to_cultivar(
    cultivar_accession=new_cultivar.cultivar_accession,
    cultivar_population=new_cultivar.cultivar_population
)
print(f"Is New Cultivar associated with Experiment B? {is_associated}")

# Unassociate the new cultivar from Experiment B
experiment_b.unassociate_cultivar(
    cultivar_accession=new_cultivar.cultivar_accession,
    cultivar_population=new_cultivar.cultivar_population
)

# Check if the new cultivar is still associated with Experiment B
is_associated = experiment_b.belongs_to_cultivar(
    cultivar_accession=new_cultivar.cultivar_accession,
    cultivar_population=new_cultivar.cultivar_population
)
print(f"Is New Cultivar still associated with Experiment B? {is_associated}")

# Create a new cultivar for Experiment B
experiment_cultivar = experiment_b.create_new_cultivar(
    cultivar_accession="Experiment B Cultivar",
    cultivar_population="Experiment B Population",
    cultivar_info={"test": "test"}
)
print(f"Created New Cultivar: {experiment_cultivar}")
