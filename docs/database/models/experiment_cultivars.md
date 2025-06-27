# Experiment Cultivars

The `experiment_cultivars` table links experiments with the cultivars being studied.

## Table Schema

| Column Name     | Data Type | Description                                             |
| --------------- | --------- | ------------------------------------------------------- |
| `experiment_id` | `UUID`    | **Primary Key, Foreign Key.** Links to `experiments.id`. |
| `cultivar_id`   | `UUID`    | **Primary Key, Foreign Key.** Links to `cultivars.id`.   |
