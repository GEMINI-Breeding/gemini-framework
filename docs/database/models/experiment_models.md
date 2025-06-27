# Experiment Models

The `experiment_models` table links experiments with the models being used.

## Table Schema

| Column Name     | Data Type | Description                                             |
| --------------- | --------- | ------------------------------------------------------- |
| `experiment_id` | `UUID`    | **Primary Key, Foreign Key.** Links to `experiments.id`. |
| `model_id`      | `UUID`    | **Primary Key, Foreign Key.** Links to `models.id`.      |
