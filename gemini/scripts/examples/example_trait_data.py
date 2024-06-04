from gemini.api import Trait, TraitRecord
from random import randint
from datetime import datetime, timedelta
import os

start_date = "2021-01-01"
end_date = "2021-01-05"
trait_name = "Average Temperature"
records_per_day = 144
avg_temp_trait = Trait.create(
    trait_name=trait_name,
    trait_units="Celsius",
    experiment_name="GEMINI",
)

# For everyday between start_date and end_date
current_date = start_date
while current_date <= end_date:

    records_to_add = []

    timestamps = []
    trait_values = []

    # 144 timestamps for that day
    for i in range(records_per_day):
        timestamp = f"{current_date} {i // 6}:{(i % 6) * 10}:00"
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        timestamps.append(timestamp)

        # Random temperature between 0 and 40
        trait_value = randint(0, 40)
        trait_values.append(trait_value)

    avg_temp_trait.add_records(
        trait_values=trait_values,
        timestamps=timestamps,
        dataset_name=f"{trait_name}_{current_date}",
        experiment_name="GEMINI",
        season_name="2021",
        site_name="Davis"
    )

    current_date = (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        
