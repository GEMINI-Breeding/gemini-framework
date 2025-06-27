# Run Views

This section describes the views related to runs, which provide simplified or aggregated access to run-related information.

## Procedure Runs View (`procedure_runs_view`)

This view combines information from procedures and procedure runs.

### View Schema

| Column Name        | Data Type      | Description                                                                                      |
| ------------------ | -------------- | ------------------------------------------------------------------------------------------------ |
| `procedure_run_id` | `UUID`         | **Primary Key.** A unique identifier for the procedure run.                                      |
| `procedure_id`     | `UUID`         | **Primary Key.** A unique identifier for the procedure.                                          |
| `procedure_name`   | `String`       | The name of the procedure.                                                                       |
| `procedure_info`   | `JSONB`        | Additional JSONB data for the procedure.                                                         |
| `procedure_run_info`| `JSONB`        | Additional JSONB data for the procedure run.                                                     |

## Script Runs View (`script_runs_view`)

This view combines information from scripts and script runs.

### View Schema

| Column Name      | Data Type      | Description                                                                                      |
| ---------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `script_run_id`  | `UUID`         | **Primary Key.** A unique identifier for the script run.                                         |
| `script_id`      | `UUID`         | **Primary Key.** A unique identifier for the script.                                             |
| `script_name`    | `String`       | The name of the script.                                                                          |
| `script_url`     | `String`       | The URL where the script can be accessed.                                                        |
| `script_extension`| `String`       | The file extension of the script.                                                                |
| `script_info`    | `JSONB`        | Additional JSONB data for the script.                                                            |
| `script_run_info`| `JSONB`        | Additional JSONB data for the script run.                                                        |

## Model Runs View (`model_runs_view`)

This view combines information from models and model runs.

### View Schema

| Column Name      | Data Type      | Description                                                                                      |
| ---------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `model_run_id`   | `UUID`         | **Primary Key.** A unique identifier for the model run.                                          |
| `model_id`       | `UUID`         | **Primary Key.** A unique identifier for the model.                                             |
| `model_name`     | `String`       | The name of the model.                                                                           |
| `model_url`      | `String`       | The URL where the model can be accessed.                                                         |
| `model_info`     | `JSONB`        | Additional JSONB data for the model.                                                             |
| `model_run_info` | `JSONB`        | Additional JSONB data for the model run.                                                         |
