# Sensor Records API

### Description

A sensor record is a record that belongs to a specific [Sensor](sensors.md), a specific [Experiment](experiments.md), [Season](seasons.md), [Site](sites.md), and [Plot](plots.md).

It is defined by the following properties:

| Property            | Type                 | Description                                     |
|---------------------|----------------------|-------------------------------------------------|
| `id`                | `UUID`               | The unique identifier of the sensor record.      |
| `timestamp`         | `datetime`           | The timestamp of the record.                    |
| `collection_date`   | `date`               | The collection date of the record.              |
| `sensor_name`       | `string`             | The name of the associated sensor.               |
| `sensor_id`         | `UUID`               | The ID of the associated sensor.                 |
| `sensor_data`       | `dict`               | The data associated with the sensor record.      |
| `dataset_id`        | `UUID`               | The ID of the associated dataset.               |
| `dataset_name`      | `string`             | The name of the associated dataset.             |
| `experiment_name`   | `string`             | The name of the associated experiment.          |
| `experiment_id`     | `UUID`               | The ID of the associated experiment.            |
| `season_name`       | `string`             | The name of the associated season.              |
| `season_id`         | `UUID`               | The ID of the associated season.                |
| `site_name`         | `string`             | The name of the associated site.                |
| `site_id`           | `UUID`               | The ID of the associated site.                  |
| `plot_id`           | `UUID`               | The ID of the associated plot.                  |
| `plot_number`       | `integer`            | The number of the associated plot.              |
| `plot_row_number`   | `integer`            | The row number of the associated plot.          |
| `plot_column_number`| `integer`            | The column number of the associated plot.       |
| `record_file`       | `string`             | The file path for the record data in the object storage. |
| `record_info`       | `dict`               | Additional information about the record.        |


A sensor record is uniquely identified within a sensor by its `timestamp`, `sensor_name`, `dataset_name`, `experiment_name`, `season_name`, `site_name`, `plot_number`, `plot_row_number` and `plot_column_number`. There will be no two sensor records with the same timestamp and belonging to the same sensor, dataset, experiment, season and site.

### Module

::: gemini.api.sensor_record