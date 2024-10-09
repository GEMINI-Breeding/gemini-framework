from gemini.api import Plot

import os
import pandas as pd
from rich.progress import track
from tqdm.auto import tqdm

plot_data_folder = os.path.join(os.path.dirname(__file__), "plot_data")
plot_data_files = os.listdir(plot_data_folder)

plot_dataframes = []
plot_dataframe = pd.DataFrame()

for plot_data_file in plot_data_files:

    df = pd.read_excel(os.path.join(plot_data_folder, plot_data_file))

    accession_column = pd.Series()
    population_column = pd.Series()
    experiment_column = pd.Series()
    season_column = pd.Series()
    site_column = pd.Series()
    info_column = pd.Series()
    tier_column = pd.Series()
    bed_column = pd.Series()

    location, year, variety = os.path.basename(plot_data_file).split(".")[0].split("_")

    info_columns = []
    info_column_names = []

    for column in df.columns:
        if column in ["Crop"]:
            cultivar_column = df[column]
        elif column in ["Genotype", "Accession", "entry.list.vect"]:
            accession_column = df[column]
        elif column in ["Bed"]:
            bed_column = df[column]
        elif column in ["Row", "Tier"]:
            tier_column = df[column]
        elif "Row.bed.number" in column:
            # Extract the Row and Bed number from the column
            # Convert it into two columns for bed and tier
            row_bed_number = df[column]
            tier_numbers = row_bed_number.str.extract("Row (\d+)", expand=False)
            bed_numbers = row_bed_number.str.extract("bed (\d+)", expand=False)

        elif column in [
            "Field.plot.number",
            "plot.number",
            "Field plots",
            "Field_PlotID",
        ]:
            plot_number_column = df[column]

        else:
            info_column = df[column]
            info_columns.append(info_column)
            info_column_names.append(column)

    if cultivar_column.empty and accession_column.empty:
        print(f"No accession and cultivar column found in {plot_data_file}")
        continue

    if plot_number_column.empty:
        print(f"No plot number column found in {plot_data_file}")
        continue

    if bed_column.empty:
        print(f"No bed number column found in {plot_data_file}")
        continue

    if tier_column.empty:
        print(f"No tier number column found in {plot_data_file}")
        continue

    cultivar_column = cultivar_column.str.title()

    # For each column in the info columns, remove Nan values and convert to empty string
    for i in range(len(info_columns)):
        info_columns[i] = info_columns[i].fillna("")

    # Convert the list of series into a series of dictionaries
    info_series = pd.Series(
        [dict(zip(info_column_names, info)) for info in zip(*info_columns)]
    )

    # Experiment column should be values al lequal to 'GEMINI'
    experiment_column = ["GEMINI"] * len(plot_number_column)

    season_column = [year] * len(plot_number_column)

    if location == "Davis":
        if variety != "Sorghum":
            # Append the site column with Davis Legumes
            locations = ["Davis Legumes"] * len(plot_number_column)
        else:
            # Append the site column with Davis Sorghum
            locations = ["Davis Sorghum"] * len(plot_number_column)
    else:
        # Append the site column with West Side
        locations = ["Kearney Legumes"] * len(plot_number_column)

    location_series = pd.Series(locations)
    site_column = pd.concat([site_column, location_series], ignore_index=True)

    plot_dataframe = pd.DataFrame()
    plot_dataframe["Accession"] = accession_column
    plot_dataframe["Population"] = cultivar_column
    plot_dataframe["Experiment"] = experiment_column
    plot_dataframe["Season"] = season_column
    plot_dataframe["Site"] = site_column
    plot_dataframe["Info"] = info_series
    plot_dataframe["Tier"] = tier_column
    plot_dataframe["Bed"] = bed_column
    plot_dataframe["Plot Number"] = plot_number_column

    plot_dataframes.append(plot_dataframe)

plot_dataframe = pd.concat(plot_dataframes)
plot_dataframe["Population"] = plot_dataframe["Population"].str.title()
plot_dataframe.fillna("", inplace=True)
plot_dataframe.reset_index(drop=True, inplace=True)
print(f"Number of plots: {len(plot_dataframe)}")

plots = []

for index, row in track(plot_dataframe.iterrows(), total=len(plot_dataframe)):
    plot = Plot.create(
        experiment_name=row["Experiment"],
        season_name=row["Season"],
        site_name=row["Site"],
        plot_number=row["Plot Number"],
        plot_info=row["Info"],
        plot_row_number=row["Tier"],
        plot_column_number=row["Bed"],
        cultivar_accession=row["Accession"],
        cultivar_population=row["Population"],
    )

    plots.append(plot)

print(f"Created {len(plots)} plots")
