# Experiment Scripts

The `experiment_scripts` table links experiments with the scripts used.

## Table Schema

| Column Name     | Data Type | Description                                             |
| --------------- | --------- | ------------------------------------------------------- |
| `experiment_id` | `UUID`    | **Primary Key, Foreign Key.** Links to `experiments.id`. |
| `script_id`     | `UUID`    | **Primary Key, Foreign Key.** Links to `scripts.id`.     |
