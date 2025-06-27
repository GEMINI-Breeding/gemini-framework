# Plots API

### Description

A plot represents an arbitrary area within a field designated for planting one or more [Plants](plants.md). Each plot is uniquely identified by its associated [Experiment](experiments.md), [Season](seasons.md), and [Site](sites.md).

It is defined by the following properties:

| Property              | Type          | Description                       |
|-----------------------|---------------|-----------------------------------|
| `id`                  | `UUID`        | The unique identifier of the plot.|
| `plot_number`         | `int`         | The number of the plot.           |
| `plot_row_number`     | `int`         | The row number of the plot.       |
| `plot_column_number`  | `int`         | The column number of the plot.    |
| `plot_geometry_info`  | `dict`        | Geometry information about the plot.|
| `plot_info`           | `dict`        | Additional information about the plot.|
| `experiment_id`       | `UUID`        | The ID of the associated experiment.|
| `season_id`           | `UUID`        | The ID of the associated season.  |
| `site_id`             | `UUID`        | The ID of the associated site.    |
| `experiment_name`     | `str`         | The name of the associated experiment.|
| `season_name`         | `str`         | The name of the associated season.|
| `site_name`           | `str`         | The name of the associated site.  |

### Module

::: gemini.api.plot