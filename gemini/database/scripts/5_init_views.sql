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
    p.plot_number AS plot_number,
    p.plot_row_number AS plot_row_number,
    p.plot_column_number AS plot_column_number,
    p.plot_info AS plot_info,
    c.id AS cultivar_id,
    c.cultivar_accession,
    c.cultivar_population
FROM
    gemini.plots p
    JOIN gemini.plot_cultivars pc ON p.id = pc.plot_id
    JOIN gemini.cultivars c ON pc.cultivar_id = c.id;

-------------------------------------------------------------------------------
-- Materialized View to show Experiment Sites
CREATE MATERIALIZED VIEW IF NOT EXISTS gemini.experiment_sites_view
USING columnar
AS
SELECT
    e.id AS experiment_id,
    e.experiment_name AS experiment_name,
    s.id AS site_id,
    s.site_name AS site_name,
    s.site_city AS site_city,
    s.site_state AS site_state,
    s.site_country AS site_country,
    s.site_info AS site_info
FROM
    gemini.experiments e
    JOIN gemini.experiment_sites es ON e.id = es.experiment_id
    JOIN gemini.sites s ON es.site_id = s.id;

-------------------------------------------------------------------------------
-- Materialized View to show Experiment Seasons
CREATE MATERIALIZED VIEW IF NOT EXISTS gemini.experiment_traits_view
USING columnar
AS
SELECT
    e.id AS experiment_id,
    e.experiment_name AS experiment_name,
    t.id AS trait_id,
    t.trait_name AS trait_name,
    t.trait_units AS trait_units,
    t.trait_metrics AS trait_metrics,
    t.trait_info AS trait_info
FROM
    gemini.experiments e
    JOIN gemini.experiment_traits et ON e.id = et.experiment_id
    JOIN gemini.traits t ON et.trait_id = t.id;

-------------------------------------------------------------------------------
-- Materialized View to show Experiment Sensors
CREATE MATERIALIZED VIEW IF NOT EXISTS gemini.experiment_sensors_view
USING columnar
AS
SELECT
    e.id AS experiment_id,
    e.experiment_name AS experiment_name,
    s.id AS sensor_id,
    s.sensor_name AS sensor_name,
    s.sensor_type_id AS sensor_type_id,
    s.sensor_platform_id AS sensor_platform_id,
    s.sensor_data_type_id AS sensor_data_type_id,
    s.sensor_data_format_id AS sensor_data_format_id,
    s.sensor_info AS sensor_info
FROM
    gemini.experiments e
    JOIN gemini.experiment_sensors es ON e.id = es.experiment_id
    JOIN gemini.sensors s ON es.sensor_id = s.id;

-------------------------------------------------------------------------------
-- Materialized View to show Experiment Cultivars
CREATE MATERIALIZED VIEW IF NOT EXISTS gemini.experiment_cultivars_view
USING columnar
AS
SELECT
    e.id AS experiment_id,
    e.experiment_name AS experiment_name,
    c.id AS cultivar_id,
    c.cultivar_accession AS cultivar_accession,
    c.cultivar_population AS cultivar_population,
    c.cultivar_info AS cultivar_info
FROM
    gemini.experiments e
    JOIN gemini.experiment_cultivars ec ON e.id = ec.experiment_id
    JOIN gemini.cultivars c ON ec.cultivar_id = c.id;


-------------------------------------------------------------------------------
-- Materialized View to show Experiment Procedures
CREATE MATERIALIZED VIEW IF NOT EXISTS gemini.experiment_procedures_view
USING columnar
AS
SELECT
    e.id AS experiment_id,
    e.experiment_name AS experiment_name,
    p.id AS procedure_id,
    p.procedure_name AS procedure_name,
    p.procedure_info AS procedure_info
FROM
    gemini.experiments e
    JOIN gemini.experiment_procedures ep ON e.id = ep.experiment_id
    JOIN gemini.procedures p ON ep.procedure_id = p.id;


-------------------------------------------------------------------------------
-- Materialized View to show Experiment Scripts
CREATE MATERIALIZED VIEW IF NOT EXISTS gemini.experiment_scripts_view
USING columnar
AS
SELECT
    e.id AS experiment_id,
    e.experiment_name AS experiment_name,
    s.id AS script_id,
    s.script_name AS script_name,
    s.script_url AS script_url,
    s.script_extension AS script_extension,
    s.script_info AS script_info
FROM
    gemini.experiments e
    JOIN gemini.experiment_scripts es ON e.id = es.experiment_id
    JOIN gemini.scripts s ON es.script_id = s.id;

-------------------------------------------------------------------------------
-- Materialized View to show Experiment Models
CREATE MATERIALIZED VIEW IF NOT EXISTS gemini.experiment_models_view
USING columnar
AS
SELECT
    e.id AS experiment_id,
    e.experiment_name AS experiment_name,
    m.id AS model_id,
    m.model_name AS model_name,
    m.model_url AS model_url,
    m.model_info AS model_info
FROM
    gemini.experiments e
    JOIN gemini.experiment_models em ON e.id = em.experiment_id
    JOIN gemini.models m ON em.model_id = m.id;

-------------------------------------------------------------------------------
-- Materialized View to show Experiment Datasets
CREATE MATERIALIZED VIEW IF NOT EXISTS gemini.experiment_datasets_view
USING columnar
AS
SELECT
    e.id AS experiment_id,
    e.experiment_name AS experiment_name,
    d.id AS dataset_id,
    d.collection_date AS collection_date,
    d.dataset_name AS dataset_name,
    d.dataset_type_id AS dataset_type_id,
    d.dataset_info AS dataset_info
FROM
    gemini.experiments e
    JOIN gemini.experiment_datasets ed ON e.id = ed.experiment_id
    JOIN gemini.datasets d ON ed.dataset_id = d.id;


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

    
-------------------------------------------------------------------------------
-- IMMV
-------------------------------------------------------------------------------

SET default_table_access_method = 'columnar';
SET max_parallel_workers = 1;

-------------------------------------------------------------------------------
-- Sensor Records IMMV
-------------------------------------------------------------------------------
SELECT create_immv('gemini.sensor_records_immv', 'select * from gemini.sensor_records');

-------------------------------------------------------------------------------
-- Trait Records IMMV
-------------------------------------------------------------------------------
SELECT create_immv('gemini.trait_records_immv', 'select * from gemini.trait_records');


SET max_parallel_workers = DEFAULT;
SET default_table_access_method = 'heap';