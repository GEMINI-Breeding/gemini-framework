from gemini.api import Cultivar

import os
import pandas as pd
from rich.progress import track
from tqdm.auto import tqdm


plot_data_folder = os.path.join(os.path.dirname(__file__), "plot_data")
plot_data_files = os.listdir(plot_data_folder)

cultivar_dataframes = []
cultivar_dataframe = pd.DataFrame()

for plot_data_file in plot_data_files:

    print(f"Processing file: {plot_data_file}")
    file_path = os.path.join(plot_data_folder, plot_data_file)

    # Read the XLSX file
    df = pd.read_excel(file_path)
    df = df.fillna("")

    cultivar_dataframe = pd.DataFrame()

    population_column = pd.Series()
    accession_column = pd.Series()

    for column in df.columns:
        if column in ["Crop"]:
            population_column = df[column]
        if column in ["Genotype", "Accession", "entry.list.vect"]:
            accession_column = df[column]

    if population_column.empty and accession_column.empty:
        print(f"No accession and cultivar column found in {plot_data_file}")
        continue

    cultivar_dataframe["Accession"] = accession_column
    cultivar_dataframe["Population"] = population_column

    cultivar_dataframes.append(cultivar_dataframe)

cultivar_dataframe = pd.concat(cultivar_dataframes)
cultivar_dataframe["Population"] = cultivar_dataframe["Population"].str.title()
cultivar_dataframe.fillna("", inplace=True)
cultivar_dataframe.drop_duplicates(inplace=True)
cultivar_dataframe.reset_index(drop=True, inplace=True)

created_cultivars = []

for index, row in track(cultivar_dataframe.iterrows(), total=len(cultivar_dataframe)):
    cultivars = Cultivar.create(
        cultivar_accession=row["Accession"],
        cultivar_population=row["Population"],
    )
    created_cultivars.append(cultivars)

print(f"Created {len(created_cultivars)} cultivars")
