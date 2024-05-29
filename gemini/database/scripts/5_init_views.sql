-------------------------------------------------------------------------------
-- Views and Materialized Views
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
-- Materialized View for Plot Information

CREATE MATERIALIZED VIEW IF NOT EXISTS gemini.plot_view
USING columnar
AS
SELECT
    p.id AS plot_id,
    e.id AS experiment_id,
    e.experiment_name,
    s.id AS season_id,
    s.season_name,
    si.id AS site_id,
    si.site_name,
    p.plot_number,
    p.plot_row_number,
    p.plot_column_number,
    p.plot_geometry_info,
    p.plot_info
FROM
    gemini.plots p
    JOIN gemini.experiments e ON p.experiment_id = e.id
    JOIN gemini.seasons s ON p.season_id = s.id
    JOIN gemini.sites si ON p.site_id = si.id;

-------------------------------------------------------------------------------
-- Materialized view that shows plot cultivar information

CREATE MATERIALIZED VIEW IF NOT EXISTS gemini.plot_cultivar_view
USING columnar
AS
SELECT
    p.id AS plot_id,
    c.id AS cultivar_id,
    c.cultivar_accession,
    c.cultivar_population
FROM
    gemini.plots p
    JOIN gemini.plot_cultivars pc ON p.id = pc.plot_id
    JOIN gemini.cultivars c ON pc.cultivar_id = c.id;


-------------------------------------------------------------------------------
-- Sensor Datasets View

CREATE MATERIALIZED VIEW IF NOT EXISTS gemini.sensor_datasets_view
AS
SELECT
    sd.sensor_id,
    s.sensor_name AS sensor_name,
    sd.dataset_id,
    d.dataset_name AS dataset_name,
    sd.info AS sensor_dataset_info
FROM
    gemini.sensor_datasets sd
    JOIN gemini.sensors s ON sd.sensor_id = s.id
    JOIN gemini.datasets d ON sd.dataset_id = d.id;

-------------------------------------------------------------------------------
-- Trait Datasets View

CREATE MATERIALIZED VIEW IF NOT EXISTS gemini.trait_datasets_view
AS
SELECT
    td.trait_id,
    t.trait_name AS trait_name,
    td.dataset_id,
    d.dataset_name AS dataset_name,
    td.info AS trait_dataset_info
FROM
    gemini.trait_datasets td
    JOIN gemini.traits t ON td.trait_id = t.id
    JOIN gemini.datasets d ON td.dataset_id = d.id;


-------------------------------------------------------------------------------
-- Procedure Datasets View

CREATE MATERIALIZED VIEW IF NOT EXISTS gemini.procedure_datasets_view
AS
SELECT
    pd.procedure_id,
    p.procedure_name AS procedure_name,
    pd.dataset_id,
    d.dataset_name AS dataset_name,
    pd.info AS procedure_dataset_info
FROM
    gemini.procedure_datasets pd
    JOIN gemini.procedures p ON pd.procedure_id = p.id
    JOIN gemini.datasets d ON pd.dataset_id = d.id;

-------------------------------------------------------------------------------
-- Script Datasets View

CREATE MATERIALIZED VIEW IF NOT EXISTS gemini.script_datasets_view
AS
SELECT
    sd.script_id,
    s.script_name AS script_name,
    sd.dataset_id,
    d.dataset_name AS dataset_name,
    sd.info AS script_dataset_info
FROM
    gemini.script_datasets sd
    JOIN gemini.scripts s ON sd.script_id = s.id
    JOIN gemini.datasets d ON sd.dataset_id = d.id;


-------------------------------------------------------------------------------
-- Model Datasets View

CREATE MATERIALIZED VIEW IF NOT EXISTS gemini.model_datasets_view
AS
SELECT
    md.model_id,
    m.model_name AS model_name,
    md.dataset_id,
    d.dataset_name AS dataset_name,
    md.info AS model_dataset_info
FROM
    gemini.model_datasets md
    JOIN gemini.models m ON md.model_id = m.id
    JOIN gemini.datasets d ON md.dataset_id = d.id;

    