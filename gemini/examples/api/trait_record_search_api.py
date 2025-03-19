from gemini.api.trait import Trait
import os
from datetime import datetime, timedelta
import random

# Create Trait X
trait = Trait.create(
    trait_name="Trait X",
    trait_info={
        "description": "Trait X for Experiment A"
    },
    experiment_name="Experiment A"
)

# Starting timestamp for records
starting_timestamp = datetime.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

# Add a single record to Trait X
success, id_list = trait.add_record(
    timestamp=starting_timestamp,
    collection_date=starting_timestamp.date(),
    trait_value=random.uniform(0, 100),
    experiment_name="Experiment A",
    season_name="Season 1A",
    site_name="Site A1",
    plot_number=990,
    plot_row_number=991,
    plot_column_number=992,
    record_info={
        "test_info": "test_value"
    }
)
print(f"Added Record Success: {success}, IDs: {id_list}")

# Add multiple records to Trait X
timestamps = [starting_timestamp + timedelta(minutes=i+1) for i in range(100)]
trait_values = [random.uniform(0, 100) for _ in range(100)]
record_info = [{"test_info": f"test_value_{i}"} for i in range(100)]
plot_numbers = [990 + i for i in range(100)]
plot_row_numbers = [991 + i for i in range(100)]
plot_column_numbers = [992 + i for i in range(100)]

success, id_list = trait.add_records(
    timestamps=timestamps,
    collection_date=starting_timestamp.date(),
    trait_values=trait_values,
    experiment_name="Experiment A",
    season_name="Season 1A",
    site_name="Site A1",
    plot_numbers=plot_numbers,
    plot_row_numbers=plot_row_numbers,
    plot_column_numbers=plot_column_numbers,
    record_info=record_info
)
print(f"Added Records Success: {success}, IDs: {id_list}")

# Search for records in Trait X
trait_records = trait.get_records(experiment_name="Experiment A")
trait_records = [record for record in trait_records]
print(f"Total Records Found: {len(trait_records)}")

