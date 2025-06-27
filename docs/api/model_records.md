# Model Records API

### Description

A model record is a record that belongs to a specific [Model](models.md), a specific [Experiment](experiments.md), [Season](seasons.md) and [Site](sites.md).

It is defined by the following properties:

| Property        | Type                 | Description                                     |
|-----------------|----------------------|-------------------------------------------------|
| `id`              | `UUID`                 | The unique identifier of the model record.      |
| `timestamp`       | `datetime`             | The timestamp of the record.                    |
| `collection_date` | `date`                 | The collection date of the record.              |
| `model_name`      | `string`               | The name of the associated model.               |
| `model_id`        | `UUID`                 | The ID of the associated model.                 |
| `model_data`      | `dict`                 | The data associated with the model record.      |
| `dataset_id`      | `UUID`                 | The ID of the associated dataset.               |
| `dataset_name`    | `string`               | The name of the associated dataset.             |
| `experiment_name` | `string`               | The name of the associated experiment.          |Mo
| `experiment_id`   | `UUID`                 | The ID of the associated experiment.            |
| `season_name`     | `string`               | The name of the associated season.              |
| `season_id`       | `UUID`                 | The ID of the associated season.                |
| `site_name`       | `string`               | The name of the associated site.                |
| `site_id`         | `UUID`                 | The ID of the associated site.                  |
| `record_file`     | `string`               | The file path for the record data in the object storage. |
| `record_info`     | `dict`                 | Additional information about the record.        |


A model record is uniquely identified within a model by its `timestamp`, `model_name`, `dataset_name`, `experiment_name`, `season_name`, and `site_name`. There will be no two model records with the same timestamp and belonging to the same model, dataset, experiment, season and site.


### Module

::: gemini.api.model_record