from gemini.api import Trait, TraitRecord
from random import randint
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os

start_date = "2021-01-01"
end_date = "2025-01-01"
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
    
    year = int(current_date[:4])

    # 144 timestamps for that day
    for i in range(records_per_day):
        timestamp = f"{current_date} {i // 6}:{(i % 6) * 10}:00"
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        timestamps.append(timestamp)

        # Random temperature between 0 and 40
        trait_value = randint(0, 40)
        trait_values.append(trait_value)

    added_records = avg_temp_trait.add_records(
        trait_values=trait_values,
        timestamps=timestamps,
        dataset_name=f"{trait_name}_{current_date}",
        experiment_name="GEMINI",
        season_name=year,
        site_name="Davis"
    )

    for record in added_records:
        print(record)

    # Go to next season
    current_date = datetime.strptime(current_date, "%Y-%m-%d") + relativedelta(years=1)
    current_date = current_date.strftime("%Y-%m-%d")
        
