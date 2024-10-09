from gemini.api import Trait

import os
import pandas as pd
from datetime import datetime

traits_file = os.path.join(
    os.path.dirname(__file__), "trait_data", "compiled_trait_data.csv"
)

df = pd.read_csv(traits_file)

# Change names of columns
df.rename(
    columns={
        "Avg_Height_Drone_cm": "Average Height from Drone",
        "Average_Height_from_Rover_cm": "Average Height from Rover",
        "Vegetation_Fraction": "Vegetation Fraction",
        "Avg_Temp_C": "Average Temperature",
        "Average_Leaf_Area_cm2": "Average Leaf Area",
        "Average_Pod_Count": "Average Pod Count",
        "Average_Leaf_Count": "Average Leaf Count",
        "Average_Flower_Count": "Average Flower Count",
    },
    inplace=True,
)

# Remove all records where "Group" is "CB-tepary"
df = df[df["Group"] != "CB-tepary"]

print(df)


avg_temp_trait = Trait.get_by_name("Average Temperature")
avg_height_drone_trait = Trait.get_by_name("Average Height from Drone")
avg_height_rover_trait = Trait.get_by_name("Average Height from Rover")
vegetation_fraction_trait = Trait.get_by_name("Vegetation Fraction")
avg_leaf_area_trait = Trait.get_by_name("Average Leaf Area")
avg_pod_count_trait = Trait.get_by_name("Average Pod Count")
avg_leaf_count_trait = Trait.get_by_name("Average Leaf Count")
avg_flower_count_trait = Trait.get_by_name("Average Flower Count")

records = {
    "avg_temp_trait": [],
    "avg_height_drone_trait": [],
    "avg_height_rover_trait": [],
    "vegetation_fraction_trait": [],
    "avg_leaf_area_trait": [],
    "avg_pod_count_trait": [],
    "avg_leaf_count_trait": [],
    "avg_flower_count_trait": [],
}

timestamps = []
plot_row_numbers = []
plot_column_numbers = []

records["avg_temp_trait"] = df["Average Temperature"].tolist()
records["avg_height_drone_trait"] = df["Average Height from Drone"].tolist()
records["avg_height_rover_trait"] = df["Average Height from Rover"].tolist()
records["vegetation_fraction_trait"] = df["Vegetation Fraction"].tolist()
records["avg_leaf_area_trait"] = df["Average Leaf Area"].tolist()
records["avg_pod_count_trait"] = df["Average Pod Count"].tolist()
records["avg_leaf_count_trait"] = df["Average Leaf Count"].tolist()
records["avg_flower_count_trait"] = df["Average Flower Count"].tolist()

timestamps = df["Date"].tolist()
timestamps = [datetime.strptime(timestamp, "%m/%d/%Y") for timestamp in timestamps]
plot_row_numbers = df["Bed"].tolist()
plot_column_numbers = df["Tier"].tolist()
plot_numbers = df["Plot"].tolist()

avg_temp_trait.add_records(
    timestamps=timestamps,
    record_data=records["avg_temp_trait"],
    plot_row_numbers=plot_row_numbers,
    plot_column_numbers=plot_column_numbers,
    plot_numbers=plot_numbers,
    experiment_name="GEMINI",
    season_name="2022",
    site_name="Davis",
)

avg_height_drone_trait.add_records(
    timestamps=timestamps,
    record_data=records["avg_height_drone_trait"],
    plot_row_numbers=plot_row_numbers,
    plot_column_numbers=plot_column_numbers,
    plot_numbers=plot_numbers,
    experiment_name="GEMINI",
    season_name="2022",
    site_name="Davis",
)

avg_height_rover_trait.add_records(
    timestamps=timestamps,
    record_data=records["avg_height_rover_trait"],
    plot_row_numbers=plot_row_numbers,
    plot_column_numbers=plot_column_numbers,
    plot_numbers=plot_numbers,
    experiment_name="GEMINI",
    season_name="2022",
    site_name="Davis",
)

vegetation_fraction_trait.add_records(
    timestamps=timestamps,
    record_data=records["vegetation_fraction_trait"],
    plot_row_numbers=plot_row_numbers,
    plot_column_numbers=plot_column_numbers,
    plot_numbers=plot_numbers,
    experiment_name="GEMINI",
    season_name="2022",
    site_name="Davis",
)

avg_leaf_area_trait.add_records(
    timestamps=timestamps,
    record_data=records["avg_leaf_area_trait"],
    plot_row_numbers=plot_row_numbers,
    plot_column_numbers=plot_column_numbers,
    plot_numbers=plot_numbers,
    experiment_name="GEMINI",
    season_name="2022",
    site_name="Davis",
)

avg_pod_count_trait.add_records(
    timestamps=timestamps,
    record_data=records["avg_pod_count_trait"],
    plot_row_numbers=plot_row_numbers,
    plot_column_numbers=plot_column_numbers,
    plot_numbers=plot_numbers,
    experiment_name="GEMINI",
    season_name="2022",
    site_name="Davis",
)

avg_leaf_count_trait.add_records(
    timestamps=timestamps,
    record_data=records["avg_leaf_count_trait"],
    plot_row_numbers=plot_row_numbers,
    plot_column_numbers=plot_column_numbers,
    plot_numbers=plot_numbers,
    experiment_name="GEMINI",
    season_name="2022",
    site_name="Davis",
)

avg_flower_count_trait.add_records(
    timestamps=timestamps,
    record_data=records["avg_flower_count_trait"],
    plot_row_numbers=plot_row_numbers,
    plot_column_numbers=plot_column_numbers,
    plot_numbers=plot_numbers,
    experiment_name="GEMINI",
    season_name="2022",
    site_name="Davis",
)

print("Records added successfully!")
