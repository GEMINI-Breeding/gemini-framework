# Experiment Procedures

The `experiment_procedures` table links experiments with the procedures followed.

## Table Schema

| Column Name      | Data Type | Description                                               |
| ---------------- | --------- | --------------------------------------------------------- |
| `experiment_id`  | `UUID`    | **Primary Key, Foreign Key.** Links to `experiments.id`.   |
| `procedure_id`   | `UUID`    | **Primary Key, Foreign Key.** Links to `procedures.id`.    |
