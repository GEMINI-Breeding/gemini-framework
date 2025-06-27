# Validation Views

This section describes the views related to validation, which provide simplified or aggregated access to validation-related information.

## Valid Plot Combinations View

The `ValidPlotCombinationsView` table combines information from plots, experiments, seasons and sites to validate plot combinations.

### Table Schema

| Column Name          | Data Type      | Description                                                                                      |
| -------------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `plot_id`             | `UUID`         | **Primary Key.** A unique identifier for the plot.                                              |
| `plot_number`        | `Integer`      | The number of the plot.                                                                          |
| `plot_row_number`    | `Integer`      | The row number of the plot in a grid layout.                                                     |
| `plot_column_number` | `Integer`      | The column number of the plot in a grid layout.                                                  |
| `plot_info`          | `JSONB`        | Additional JSONB data describing the plot.                                                       |
| `plot_geometry_info` | `JSONB`        | Additional JSONB data describing the plot's geometry.                                           |
| `experiment_id`      | `UUID`         |  Unique identifier for the experiment to which the plot belongs.                                  |
| `experiment_name`    | `String`       | The name of the experiment.                                                                      |
| `season_id`          | `UUID`         |  Unique identifier for the season during which the plot was used.                                 |
| `site_id`            | `UUID`         |  Unique identifier for the site where the plot is located.                                        |
| `site_name`          | `String`       | The name of the site.                                                                            |

## Valid Dataset Combinations View

The `ValidDatasetCombinationsView` table combines information from datasets, experiments, seasons and sites to validate dataset combinations.

### Table Schema

| Column Name          | Data Type      | Description                                                                                      |
| -------------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `dataset_id`          | `UUID`         | **Primary Key.** A unique identifier for the dataset.                                              |
| `dataset_name`        | `String`       | The name of the dataset.                                                                         |
| `dataset_info`        | `JSONB`        | Additional JSONB data describing the dataset.                                                       |
| `experiment_id`      | `UUID`         |  Unique identifier for the experiment to which the dataset belongs.                                  |
| `experiment_name`    | `String`       | The name of the experiment.                                                                      |
| `season_id`          | `UUID`         |  Unique identifier for the season during which the dataset was used.                                 |
| `site_id`            | `UUID`         |  Unique identifier for the site where the dataset is located.                                        |
| `site_name`          | `String`       | The name of the site.                                                                            |

## Valid Sensor Dataset Combinations View

The `ValidSensorDatasetCombinationsView` table combines information from sensors and datasets to validate sensor dataset combinations.

## Table Schema

| Column Name          | Data Type      | Description                                                                                      |
| -------------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `sensor_id`          | `UUID`         | **Primary Key.** A unique identifier for the sensor.                                              |
| `sensor_name`        | `String`       | The name of the sensor.                                                                          |
| `sensor_type_id`     | `Integer`      | The sensor type id.                                                                              |
| `dataset_id`          | `UUID`         | **Primary Key.** A unique identifier for the dataset.                                              |
| `dataset_name`        | `String`       | The name of the dataset.                                                                         |
| `dataset_type_id`      | `Integer`      | The dataset type id.                                                                             |

## Valid Trait Dataset Combinations View

The `ValidTraitDatasetCombinationsView` table combines information from traits and datasets to validate trait dataset combinations.

## Table Schema

| Column Name          | Data Type      | Description                                                                                      |
| -------------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `trait_id`           | `UUID`         | **Primary Key.** A unique identifier for the trait.                                               |
| `trait_name`         | `String`       | The name of the trait.                                                                           |
| `trait_units`        | `String`       | The units of the trait.                                                                          |
| `trait_level_id`     | `Integer`      | The trait level id.                                                                              |
| `dataset_id`          | `UUID`         | **Primary Key.** A unique identifier for the dataset.                                              |
| `dataset_name`        | `String`       | The name of the dataset.                                                                         |
| `dataset_type_id`      | `Integer`      | The dataset type id.                                                                             |

## Valid Procedure Dataset Combinations View

The `ValidProcedureDatasetCombinationsView` table combines information from procedures and datasets to validate procedure dataset combinations.

## Table Schema

| Column Name          | Data Type      | Description                                                                                      |
| -------------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `procedure_id`       | `UUID`         | **Primary Key.** A unique identifier for the procedure.                                           |
| `procedure_name`     | `String`       | The name of the procedure.                                                                       |
| `dataset_id`          | `UUID`         | **Primary Key.** A unique identifier for the dataset.                                              |
| `dataset_name`        | `String`       | The name of the dataset.                                                                         |
| `dataset_type_id`      | `Integer`      | The dataset type id.                                                                             |

## Valid Model Dataset Combinations View

The `ValidModelDatasetCombinationsView` table combines information from models and datasets to validate model dataset combinations.

## Table Schema

| Column Name          | Data Type      | Description                                                                                      |
| -------------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `model_id`           | `UUID`         | **Primary Key.** A unique identifier for the model.                                               |
| `model_name`         | `String`       | The name of the model.                                                                           |
| `dataset_id`          | `UUID`         | **Primary Key.** A unique identifier for the dataset.                                              |
| `dataset_name`        | `String`       | The name of the dataset.                                                                         |
| `dataset_type_id`      | `Integer`      | The dataset type id.                                                                             |

## Valid Script Dataset Combinations View

The `ValidScriptDatasetCombinationsView` table combines information from scripts and datasets to validate script dataset combinations.

## Table Schema

| Column Name          | Data Type      | Description                                                                                      |
| -------------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `script_id`          | `UUID`         | **Primary Key.** A unique identifier for the script.                                              |
| `script_name`        | `String`       | The name of the script.                                                                          |
| `dataset_id`          | `UUID`         | **Primary Key.** A unique identifier for the dataset.                                              |
| `dataset_name`        | `String`       | The name of the dataset.                                                                         |
| `dataset_type_id`      | `Integer`      | The dataset type id.                                                                             |
