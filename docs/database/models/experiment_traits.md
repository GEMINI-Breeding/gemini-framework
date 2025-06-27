# Experiment Traits

The `experiment_traits` table links experiments with the traits being measured.

## Table Schema

| Column Name     | Data Type | Description                                             |
| --------------- | --------- | ------------------------------------------------------- |
| `experiment_id` | `UUID`    | **Primary Key, Foreign Key.** Links to `experiments.id`. |
| `trait_id`      | `UUID`    | **Primary Key, Foreign Key.** Links to `traits.id`.      |
