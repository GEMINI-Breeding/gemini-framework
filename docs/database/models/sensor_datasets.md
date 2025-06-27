# Sensor Datasets

The `sensor_datasets` table links sensors to the datasets they generate.

## Table Schema

| Column Name  | Data Type | Description                                           |
| ------------ | --------- | ----------------------------------------------------- |
| `sensor_id`  | `UUID`    | **Primary Key, Foreign Key.** Links to `sensors.id`.   |
| `dataset_id` | `UUID`    | **Primary Key, Foreign Key.** Links to `datasets.id`.  |
