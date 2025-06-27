# Script Records API

### Description

A script record is a record that belongs to a specific [Script](scripts.md), a specific [Experiment](experiments.md), [Season](seasons.md) and [Site](sites.md).

It is defined by the following properties:

| Property        | Type                 | Description                                     |
|-----------------|----------------------|-------------------------------------------------|
| `id`              | `UUID`                 | The unique identifier of the script record.      |
| `timestamp`       | `datetime`             | The timestamp of the record.                    |
| `collection_date` | `date`                 | The collection date of the record.              |
| `script_name`      | `string`               | The name of the associated script.               |
| `script_id`        | `UUID`                 | The ID of the associated script.                 |
| `script_data`      | `dict`                 | The data associated with the script record.      |
| `dataset_id`      | `UUID`                 | The ID of the associated dataset.               |
| `dataset_name`    | `string`               | The name of the associated dataset.             |
| `experiment_name` | `string`               | The name of the associated experiment.          |
| `experiment_id`   | `UUID`                 | The ID of the associated experiment.            |
| `season_name`     | `string`               | The name of the associated season.              |
| `season_id`       | `UUID`                 | The ID of the associated season.                |
| `site_name`       | `string`               | The name of the associated site.                |
| `site_id`         | `UUID`                 | The ID of the associated site.                  |
| `record_file`     | `string`               | The file path for the record data in the object storage. |
| `record_info`     | `dict`                 | Additional information about the record.        |


A script record is uniquely identified within a script by its `timestamp`, `script_name`, `dataset_name`, `experiment_name`, `season_name`, and `site_name`. There will be no two script records with the same timestamp and belonging to the same script, dataset, experiment, season and site.


### Module

::: gemini.api.script_record