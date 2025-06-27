# Dataset Views

This section describes the views related to datasets, which provide simplified or aggregated access to dataset-related information.

## Sensor Datasets View (`sensor_datasets_view`)

This view combines information from sensors and datasets to show which sensors are associated with which datasets.

### View Schema

| Column Name         | Data Type   | Description                                      |
| ------------------- | ----------- | ------------------------------------------------ |
| `sensor_id`         | `UUID`      | Unique identifier for the sensor.                |
| `sensor_name`       | `String`    | The name of the sensor.                          |
| `dataset_id`        | `UUID`      | Unique identifier for the dataset.               |
| `dataset_name`      | `String`    | The name of the dataset.                         |
| `dataset_info`      | `JSONB`     | Additional JSONB data for the dataset.           |
| `collection_date`   | `DATE`      | The date when the data was collected.            |
| `dataset_type_id`   | `Integer`   | Foreign key referencing the dataset type.        |
| `sensor_dataset_info` | `JSONB`     | Additional JSONB data for the sensor-dataset association. |

## Trait Datasets View (`trait_datasets_view`)

This view combines information from traits and datasets to show which traits are associated with which datasets.

### View Schema

| Column Name         | Data Type   | Description                                      |
| ------------------- | ----------- | ------------------------------------------------ |
| `trait_id`          | `UUID`      | Unique identifier for the trait.                 |
| `trait_name`        | `String`    | The name of the trait.                           |
| `dataset_id`        | `UUID`      | Unique identifier for the dataset.               |
| `dataset_name`      | `String`    | The name of the dataset.                         |
| `dataset_info`      | `JSONB`     | Additional JSONB data for the dataset.           |
| `collection_date`   | `DATE`      | The date when the data was collected.            |
| `dataset_type_id`   | `Integer`   | Foreign key referencing the dataset type.        |
| `trait_dataset_info` | `JSONB`     | Additional JSONB data for the trait-dataset association. |

## Procedure Datasets View (`procedure_datasets_view`)

This view combines information from procedures and datasets to show which procedures are associated with which datasets.

### View Schema

| Column Name           | Data Type   | Description                                      |
| --------------------- | ----------- | ------------------------------------------------ |
| `procedure_id`        | `UUID`      | Unique identifier for the procedure.             |
| `procedure_name`      | `String`    | The name of the procedure.                       |
| `dataset_id`          | `UUID`      | Unique identifier for the dataset.               |
| `dataset_name`        | `String`    | The name of the dataset.                         |
| `dataset_info`        | `JSONB`     | Additional JSONB data for the dataset.           |
| `collection_date`     | `DATE`      | The date when the data was collected.            |
| `dataset_type_id`     | `Integer`   | Foreign key referencing the dataset type.        |
| `procedure_dataset_info` | `JSONB`     | Additional JSONB data for the procedure-dataset association. |

## Script Datasets View (`script_datasets_view`)

This view combines information from scripts and datasets to show which scripts are associated with which datasets.

### View Schema

| Column Name         | Data Type   | Description                                      |
| ------------------- | ----------- | ------------------------------------------------ |
| `script_id`         | `UUID`      | Unique identifier for the script.                |
| `script_name`       | `String`    | The name of the script.                          |
| `dataset_id`        | `UUID`      | Unique identifier for the dataset.               |
| `dataset_name`      | `String`    | The name of the dataset.                         |
| `dataset_info`      | `JSONB`     | Additional JSONB data for the dataset.           |
| `collection_date`   | `DATE`      | The date when the data was collected.            |
| `dataset_type_id`   | `Integer`   | Foreign key referencing the dataset type.        |
| `script_dataset_info` | `JSONB`     | Additional JSONB data for the script-dataset association. |

## Model Datasets View (`model_datasets_view`)

This view combines information from models and datasets to show which models are associated with which datasets.

### View Schema

| Column Name         | Data Type   | Description                                      |
| ------------------- | ----------- | ------------------------------------------------ |
| `model_id`          | `UUID`      | Unique identifier for the model.                 |
| `model_name`        | `String`    | The name of the model.                           |
| `dataset_id`        | `UUID`      | Unique identifier for the dataset.               |
| `dataset_name`      | `String`    | The name of the dataset.                         |
| `dataset_info`      | `JSONB`     | Additional JSONB data for the dataset.           |
| `collection_date`   | `DATE`      | The date when the data was collected.            |
| `dataset_type_id`   | `Integer`   | Foreign key referencing the dataset type.        |
| `model_dataset_info` | `JSONB`     | Additional JSONB data for the model-dataset association. |
