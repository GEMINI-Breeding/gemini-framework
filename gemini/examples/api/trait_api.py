from gemini.api.trait_record import TraitRecord
from gemini.api.trait import Trait
from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site

from random import randint

experiment = Experiment.get(experiment_name="Test Experiment 1")
season = Season.get(season_name="Test Season 1", experiment_name="Test Experiment 1")
site = Site.get(site_name="Test Site 1")

test_trait = Trait.get(trait_name="Test Trait 1")
print(test_trait)

trait_records = []
for i in range(1000):
    record = TraitRecord(
        timestamp=f"2021-01-01T00:00:00.{i:03d}Z",
        collection_date="2021-01-01",
        trait_id=test_trait.id,
        trait_name=test_trait.trait_name,
        trait_value=randint(0, 100),
        experiment_id=experiment.id,
        experiment_name=experiment.experiment_name,
        season_id=season.id,
        season_name=season.season_name,
        site_id=site.id,
        site_name=site.site_name,
        record_info={}
    )
    trait_records.append(record)

print(trait_records)

# Add Records to the Trait
success = test_trait.add_records(records=trait_records)