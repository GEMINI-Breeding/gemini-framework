# Experiment Sensor Platforms

The `experiment_sensor_platforms` table links experiments with the sensor platforms used.

## Table Schema

| Column Name          | Data Type | Description                                                    |
| -------------------- | --------- | -------------------------------------------------------------- |
| `experiment_id`      | `UUID`    | **Primary Key, Foreign Key.** Links to `experiments.id`.        |
| `sensor_platform_id` | `UUID`    | **Primary Key, Foreign Key.** Links to `sensor_platforms.id`.   |
