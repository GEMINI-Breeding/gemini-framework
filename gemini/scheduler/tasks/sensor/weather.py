from prefect import task
from datetime import datetime
import os 

@task
def process_weather_data(file_path: str, **kwargs) -> dict:
    with open(file_path, "r") as f:
        lines = f.readlines()

        column_names = lines[1].strip().split(",")
        column_names = [column_name.strip('"') for column_name in column_names]

        units = lines[2].strip().split(",")
        units = [unit.strip('"') for unit in units]

        timestamps = []
        records_to_add = []

        for line in lines[4:]:
            data = line.strip().split(",")
            data = [value.strip('"') for value in data]

            timestamp = datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S")
            timestamps.append(timestamp)

            collection_date = timestamp.date()
            record_data = dict(zip(column_names[2:], data[2:]))
            records_to_add.append(record_data)

        return {
            "timestamps": timestamps,
            "collection_date": collection_date,
            "records": records_to_add
        }

