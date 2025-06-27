# Plot Cultivar View

The `plot_cultivar_view` table combines information from plots and cultivars.

## Table Schema

| Column Name           | Data Type      | Description                                                                                      |
| --------------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `plot_id`             | `UUID`         | **Primary Key.** A unique identifier for the plot.                                              |
| `plot_number`        | `Integer`      | The number of the plot.                                                                          |
| `plot_row_number`    | `Integer`      | The row number of the plot in a grid layout.                                                     |
| `plot_column_number` | `Integer`      | The column number of the plot in a grid layout.                                                  |
| `plot_info`          | `JSONB`        | Additional JSONB data describing the plot.                                                       |
| `plot_geometry_info` | `JSONB`        | Additional JSONB data describing the plot's geometry.                                           |
| `experiment_id`      | `UUID`         |  Unique identifier for the experiment to which the plot belongs.                                  |
| `experiment_name`    | `String`       | The name of the experiment.                                                                      |
| `season_id`          | `UUID`         |  Unique identifier for the season during which the plot was used.                                 |
| `season_name`        | `String`       | The name of the season.                                                                          |
| `site_id`            | `UUID`         |  Unique identifier for the site where the plot is located.                                        |
| `site_name`          | `String`       | The name of the site.                                                                            |
| `cultivar_id`         | `UUID`         |  Unique identifier for the cultivar.                                                              |
| `cultivar_accession`  | `String`       | The accession identifier for the cultivar.                                                       |
| `cultivar_population` | `String`       | The population name of the cultivar.                                                             |
| `cultivar_info`       | `JSONB`         | Additional JSONB data for the cultivar.                                                              |
