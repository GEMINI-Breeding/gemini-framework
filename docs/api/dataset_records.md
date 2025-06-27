# Dataset Records API

### Description

A dataset record is a record that belongs to a specific [Dataset](datasets.md), a specific [Experiment](experiments.md), [Season](seasons.md) and [Site](sites.md).

It is defined by the following properties:
| Property        | Type                 | Description                               |
|-----------------|----------------------|-------------------------------------------|
| `id`            | `UUID`               | The unique identifier of the dataset record. |
| `timestamp`     | `datetime`           | The timestamp of the record.              |
| `collection_date` | `date`               | The collection date of the record.        |
| `dataset_id`    | `UUID`               | The ID of the associated dataset.         |
| `dataset_name`  | `string`             | The name of the associated dataset.       |
| `dataset_data`  | `dict`               | The data content of the record.           |
| `experiment_name` | `string`             | The name of the associated experiment.    |
| `experiment_id` | `UUID`               | The ID of the associated experiment.      |
| `season_name`   | `string`             | The name of the associated season.        |
| `season_id`     | `UUID`               | The ID of the associated season.          |
| `site_name`     | `string`             | The name of the associated site.          |
| `site_id`       | `UUID`               | The ID of the associated site.            |
| `record_file`   | `string`             | The file path for the record data in the object storage. |
| `record_info`   | `dict`               | Additional information about the record.  |

A dataset record is uniquely identified within a dataset by its `timestamp`, `dataset_name`, `experiment_name`, `season_name`, and `site_name`. There will be no two dataset records with the same timestamp and belonging to the same dataset, experiment, season and site.

### Module

::: gemini.api.dataset_record