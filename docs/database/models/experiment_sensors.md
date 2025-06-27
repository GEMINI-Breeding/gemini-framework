# Experiment Sensors

The `experiment_sensors` table links experiments with the sensors used.

## Table Schema

| Column Name     | Data Type | Description                                             |
| --------------- | --------- | ------------------------------------------------------- |
| `experiment_id` | `UUID`    | **Primary Key, Foreign Key.** Links to `experiments.id`. |
| `sensor_id`     | `UUID`    | **Primary Key, Foreign Key.** Links to `sensors.id`.     |
