-------------------------------------------------------------------------------
-- Views and Materialized Views
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
-- View for plot entity combinations
CREATE OR REPLACE VIEW gemini.valid_plot_combinations_view AS
SELECT
    e.id AS experiment_id,
    e.experiment_name AS experiment_name,
    s.id AS season_id,
    s.season_name AS season_name,
    si.id AS site_id,
    si.site_name AS site_name
FROM gemini.experiments AS e
JOIN gemini.seasons AS s
    ON e.id = s.experiment_id
JOIN gemini.experiment_sites AS es
    ON e.id = es.experiment_id
JOIN gemini.sites AS si
    ON es.site_id = si.id;


-------------------------------------------------------------------------------
-- View for storing valid combinations of datasets, experiments, seasons, and sites
CREATE OR REPLACE VIEW gemini.valid_dataset_combinations_view AS
SELECT
    d.dataset_name,
    e.experiment_name,
    s.season_name,
    si.site_name
FROM gemini.datasets AS d
JOIN gemini.experiment_datasets AS ed
    ON d.id = ed.dataset_id
JOIN gemini.experiments AS e
    ON ed.experiment_id = e.id
JOIN gemini.seasons AS s
    ON e.id = s.experiment_id
JOIN gemini.experiment_sites AS es
    ON e.id = es.experiment_id
JOIN gemini.sites AS si
    ON es.site_id = si.id;

-------------------------------------------------------------------------------
-- View for sensor combinations
CREATE OR REPLACE VIEW gemini.valid_sensor_dataset_combinations_view AS
SELECT
    d.dataset_name,
    se.sensor_name,
    e.experiment_name,
    s.season_name,
    si.site_name
FROM gemini.datasets AS d
JOIN gemini.sensor_datasets AS sd
    ON d.id = sd.dataset_id
JOIN gemini.sensors AS se
    ON sd.sensor_id = se.id
JOIN gemini.experiment_datasets AS ed
    ON d.id = ed.dataset_id
JOIN gemini.experiments AS e
    ON ed.experiment_id = e.id
JOIN gemini.seasons AS s
    ON e.id = s.experiment_id
JOIN gemini.experiment_sites AS es
    ON e.id = es.experiment_id
JOIN gemini.sites AS si
    ON es.site_id = si.id;

-------------------------------------------------------------------------------
-- View for trait combinations
CREATE OR REPLACE VIEW gemini.valid_trait_dataset_combinations_view AS
SELECT
    d.dataset_name,
    t.trait_name,
    e.experiment_name,
    s.season_name,
    si.site_name
FROM gemini.datasets AS d
JOIN gemini.trait_datasets AS td
    ON d.id = td.dataset_id
JOIN gemini.traits AS t
    ON td.trait_id = t.id
JOIN gemini.experiment_datasets AS ed
    ON d.id = ed.dataset_id
JOIN gemini.experiments AS e
    ON ed.experiment_id = e.id
JOIN gemini.seasons AS s
    ON e.id = s.experiment_id
JOIN gemini.experiment_sites AS es
    ON e.id = es.experiment_id
JOIN gemini.sites AS si
    ON es.site_id = si.id;

-------------------------------------------------------------------------------
-- View for procedure combinations
CREATE OR REPLACE VIEW gemini.valid_procedure_dataset_combinations_view AS
SELECT
    d.dataset_name,
    p.procedure_name,
    e.experiment_name,
    s.season_name,
    si.site_name
FROM gemini.datasets AS d
JOIN gemini.procedure_datasets AS pd
    ON d.id = pd.dataset_id
JOIN gemini.procedures AS p
    ON pd.procedure_id = p.id
JOIN gemini.experiment_datasets AS ed
    ON d.id = ed.dataset_id
JOIN gemini.experiments AS e
    ON ed.experiment_id = e.id
JOIN gemini.seasons AS s
    ON e.id = s.experiment_id
JOIN gemini.experiment_sites AS es
    ON e.id = es.experiment_id
JOIN gemini.sites AS si
    ON es.site_id = si.id;

-------------------------------------------------------------------------------
-- View for script combinations
CREATE OR REPLACE VIEW gemini.valid_script_dataset_combinations_view AS
SELECT
    d.dataset_name,
    sc.script_name,
    e.experiment_name,
    s.season_name,
    si.site_name
FROM gemini.datasets AS d
JOIN gemini.script_datasets AS sd
    ON d.id = sd.dataset_id
JOIN gemini.scripts AS sc
    ON sd.script_id = sc.id
JOIN gemini.experiment_datasets AS ed
    ON d.id = ed.dataset_id
JOIN gemini.experiments AS e
    ON ed.experiment_id = e.id
JOIN gemini.seasons AS s
    ON e.id = s.experiment_id
JOIN gemini.experiment_sites AS es
    ON e.id = es.experiment_id
JOIN gemini.sites AS si
    ON es.site_id = si.id;

-------------------------------------------------------------------------------
-- View for model combinations
CREATE OR REPLACE VIEW gemini.valid_model_dataset_combinations_view AS
SELECT
    d.dataset_name,
    m.model_name,
    e.experiment_name,
    s.season_name,
    si.site_name
FROM gemini.datasets AS d
JOIN gemini.model_datasets AS md
    ON d.id = md.dataset_id
JOIN gemini.models AS m
    ON md.model_id = m.id
JOIN gemini.experiment_datasets AS ed
    ON d.id = ed.dataset_id
JOIN gemini.experiments AS e
    ON ed.experiment_id = e.id
JOIN gemini.seasons AS s
    ON e.id = s.experiment_id
JOIN gemini.experiment_sites AS es
    ON e.id = es.experiment_id
JOIN gemini.sites AS si
    ON es.site_id = si.id;


-------------------------------------------------------------------------------
-- View for sites and their associated plots
CREATE OR REPLACE VIEW gemini.site_plot_view AS
SELECT
    s.site_name,
    p.id as plot_id,
    p.plot_number,
    p.plot_row_number,
    p.plot_column_number,
    p.plot_geometry_info,
    p.plot_info
FROM gemini.sites AS s
JOIN gemini.plots AS p
    ON s.id = p.site_id;

-------------------------------------------------------------------------------
-- View for plots and respective plants
CREATE OR REPLACE VIEW gemini.plot_plant_view AS
SELECT
    p.id as plot_id,
    p.plot_number,
    p.plot_row_number,
    p.plot_column_number,
    p.plot_geometry_info,
    p.plot_info,
    pl.id as plant_id,  
    pl.plant_number,
    pl.plant_info,
    pl.cultivar_id,
    c.cultivar_accession,
    c.cultivar_population
FROM gemini.plots AS p
JOIN gemini.plants AS pl
    ON p.id = pl.plot_id
JOIN gemini.cultivars AS c
    ON pl.cultivar_id = c.id;


-------------------------------------------------------------------------------
-- Materialized View for Plot Information

CREATE OR REPLACE VIEW gemini.plot_view
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

CREATE OR REPLACE VIEW gemini.plot_cultivar_view
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
-- Materialized view that shows plant information
CREATE OR REPLACE VIEW gemini.plant_view
AS
SELECT
    p.id AS plant_id,
    p.plot_id AS plot_id,
    p.plant_number AS plant_number,
    p.plant_info AS plant_info,
    p.cultivar_id AS cultivar_id,
    c.cultivar_accession AS cultivar_accession,
    c.cultivar_population AS cultivar_population,
    pl.plot_number AS plot_number,
    pl.plot_row_number AS plot_row_number,
    pl.plot_column_number AS plot_column_number,
    pl.plot_info AS plot_info,
    pl.plot_geometry_info AS plot_geometry_info,
    pl.experiment_id AS experiment_id,
    e.experiment_name AS experiment_name,
    s.id AS season_id,
    s.season_name AS season_name,
    si.id AS site_id,
    si.site_name AS site_name
FROM
    gemini.plants p
    JOIN gemini.plot_cultivars pc ON p.plot_id = pc.plot_id
    JOIN gemini.cultivars c ON pc.cultivar_id = c.id
    JOIN gemini.plots pl ON p.plot_id = pl.id
    JOIN gemini.experiments e ON pl.experiment_id = e.id
    JOIN gemini.seasons s ON pl.season_id = s.id
    JOIN gemini.sites si ON pl.site_id = si.id;
    


-------------------------------------------------------------------------------
-- Materialized View to show Experiment Seasons
CREATE OR REPLACE VIEW gemini.experiment_seasons_view
AS
SELECT
    e.id AS experiment_id,
    e.experiment_name AS experiment_name,
    s.id AS season_id,
    s.season_name AS season_name,
    s.season_start_date AS season_start_date,
    s.season_end_date AS season_end_date,
    s.season_info AS season_info
FROM
    gemini.experiments e
    JOIN gemini.seasons s ON e.id = s.experiment_id;

-------------------------------------------------------------------------------
-- Materialized View to show Experiment Sites
CREATE OR REPLACE VIEW gemini.experiment_sites_view
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
CREATE OR REPLACE VIEW gemini.experiment_traits_view
AS
SELECT
    e.id AS experiment_id,
    e.experiment_name AS experiment_name,
    t.id AS trait_id,
    t.trait_name AS trait_name,
    t.trait_units AS trait_units,
    t.trait_metrics AS trait_metrics,
    t.trait_level_id AS trait_level_id,
    t.trait_info AS trait_info
FROM
    gemini.experiments e
    JOIN gemini.experiment_traits et ON e.id = et.experiment_id
    JOIN gemini.traits t ON et.trait_id = t.id;

-------------------------------------------------------------------------------
-- Materialized View to show Experiment Sensor Platforms
CREATE OR REPLACE VIEW gemini.experiment_sensor_platforms_view
AS
SELECT
    e.id AS experiment_id,
    e.experiment_name AS experiment_name,
    sp.id AS sensor_platform_id,
    sp.sensor_platform_name AS sensor_platform_name,
    sp.sensor_platform_info AS sensor_platform_info
FROM
    gemini.experiments e
    JOIN gemini.experiment_sensor_platforms esp ON e.id = esp.experiment_id
    JOIN gemini.sensor_platforms sp ON esp.sensor_platform_id = sp.id;


-------------------------------------------------------------------------------
-- Materialized View to show Experiment Sensors
CREATE OR REPLACE VIEW gemini.experiment_sensors_view
AS
SELECT
    e.id AS experiment_id,
    e.experiment_name AS experiment_name,
    s.id AS sensor_id,
    s.sensor_name AS sensor_name,
    s.sensor_type_id AS sensor_type_id,
    s.sensor_data_type_id AS sensor_data_type_id,
    s.sensor_data_format_id AS sensor_data_format_id,
    s.sensor_info AS sensor_info,
    sp.id AS sensor_platform_id,
    sp.sensor_platform_name AS sensor_platform_name,
    sp.sensor_platform_info AS sensor_platform_info
FROM
    gemini.experiments e
    JOIN gemini.experiment_sensors es ON e.id = es.experiment_id
    JOIN gemini.sensors s ON es.sensor_id = s.id
    LEFT JOIN gemini.sensor_platform_sensors sps ON s.id = sps.sensor_id
    LEFT JOIN gemini.sensor_platforms sp ON sps.sensor_platform_id = sp.id;

-------------------------------------------------------------------------------
-- Materialized View to show Experiment Cultivars
CREATE OR REPLACE VIEW gemini.experiment_cultivars_view
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
CREATE OR REPLACE VIEW gemini.experiment_procedures_view
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
CREATE OR REPLACE VIEW gemini.experiment_scripts_view
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
CREATE OR REPLACE VIEW gemini.experiment_models_view
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
CREATE OR REPLACE VIEW gemini.experiment_datasets_view
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

CREATE OR REPLACE VIEW gemini.sensor_datasets_view
AS
SELECT
    sd.sensor_id,
    s.sensor_name AS sensor_name,
    sd.dataset_id,
    d.dataset_name AS dataset_name,
    d.dataset_info AS dataset_info,
    d.collection_date AS collection_date,
    d.dataset_type_id AS dataset_type_id,
    sd.info AS sensor_dataset_info
FROM
    gemini.sensor_datasets sd
    JOIN gemini.sensors s ON sd.sensor_id = s.id
    JOIN gemini.datasets d ON sd.dataset_id = d.id;

-------------------------------------------------------------------------------
-- Trait Datasets View

CREATE OR REPLACE VIEW gemini.trait_datasets_view
AS
SELECT
    td.trait_id,
    t.trait_name AS trait_name,
    td.dataset_id,
    d.dataset_name AS dataset_name,
    d.dataset_info AS dataset_info,
    d.collection_date AS collection_date,
    d.dataset_type_id AS dataset_type_id,
    td.info AS trait_dataset_info
FROM
    gemini.trait_datasets td
    JOIN gemini.traits t ON td.trait_id = t.id
    JOIN gemini.datasets d ON td.dataset_id = d.id;


-------------------------------------------------------------------------------
-- Procedure Datasets View

CREATE OR REPLACE VIEW gemini.procedure_datasets_view
AS
SELECT
    pd.procedure_id,
    p.procedure_name AS procedure_name,
    pd.dataset_id,
    d.dataset_name AS dataset_name,
    d.dataset_info AS dataset_info,
    d.collection_date AS collection_date,
    d.dataset_type_id AS dataset_type_id,
    pd.info AS procedure_dataset_info
FROM
    gemini.procedure_datasets pd
    JOIN gemini.procedures p ON pd.procedure_id = p.id
    JOIN gemini.datasets d ON pd.dataset_id = d.id;

-------------------------------------------------------------------------------
-- Procedure Runs View

CREATE OR REPLACE VIEW gemini.procedure_runs_view
AS
SELECT
    pr.id AS procedure_run_id,
    pr.procedure_id AS procedure_id,
    p.procedure_name AS procedure_name,
    p.procedure_info AS procedure_info,
    pr.procedure_run_info AS procedure_run_info
FROM
    gemini.procedure_runs pr
    JOIN gemini.procedures p ON pr.procedure_id = p.id;


-------------------------------------------------------------------------------
-- Script Datasets View

CREATE OR REPLACE VIEW gemini.script_datasets_view
AS
SELECT
    sd.script_id,
    s.script_name AS script_name,
    sd.dataset_id,
    d.dataset_name AS dataset_name,
    d.dataset_info AS dataset_info,
    d.collection_date AS collection_date,
    d.dataset_type_id AS dataset_type_id,
    sd.info AS script_dataset_info
FROM
    gemini.script_datasets sd
    JOIN gemini.scripts s ON sd.script_id = s.id
    JOIN gemini.datasets d ON sd.dataset_id = d.id;

------------------------------------------------------------------------------
-- Script Runs View

CREATE OR REPLACE VIEW gemini.script_runs_view
AS
SELECT
    sr.id AS script_run_id,
    sr.script_id AS script_id,
    s.script_name AS script_name,
    s.script_url AS script_url,
    s.script_extension AS script_extension,
    s.script_info AS script_info,
    sr.script_run_info AS script_run_info
FROM
    gemini.script_runs sr
    JOIN gemini.scripts s ON sr.script_id = s.id;


-------------------------------------------------------------------------------
-- Model Datasets View

CREATE OR REPLACE VIEW gemini.model_datasets_view
AS
SELECT
    md.model_id,
    m.model_name AS model_name,
    md.dataset_id,
    d.dataset_name AS dataset_name,
    d.dataset_info AS dataset_info,
    d.collection_date AS collection_date,
    d.dataset_type_id AS dataset_type_id,
    md.info AS model_dataset_info
FROM
    gemini.model_datasets md
    JOIN gemini.models m ON md.model_id = m.id
    JOIN gemini.datasets d ON md.dataset_id = d.id;


-----------------------------------------------------------------------------------
-- Model Runs View

CREATE OR REPLACE VIEW gemini.model_runs_view
AS
SELECT
    mr.id AS model_run_id,
    mr.model_id AS model_id,
    m.model_name AS model_name,
    m.model_url AS model_url,
    m.model_info AS model_info,
    mr.model_run_info AS model_run_info
FROM
    gemini.model_runs mr
    JOIN gemini.models m ON mr.model_id = m.id;

    
-------------------------------------------------------------------------------
-- IMMV
-------------------------------------------------------------------------------

SET default_table_access_method = 'columnar';
SET max_parallel_workers = 1;

-------------------------------------------------------------------------------
-- Sensor Records IMMV
-------------------------------------------------------------------------------
SELECT pgivm.create_immv('gemini.sensor_records_immv', 'select * from gemini.sensor_records');

-------------------------------------------------------------------------------
-- Trait Records IMMV
-------------------------------------------------------------------------------
SELECT pgivm.create_immv('gemini.trait_records_immv', 'select * from gemini.trait_records');

-------------------------------------------------------------------------------
-- Procedure Records IMMV
-------------------------------------------------------------------------------
SELECT pgivm.create_immv('gemini.procedure_records_immv', 'select * from gemini.procedure_records');

-------------------------------------------------------------------------------
-- Script Records IMMV
-------------------------------------------------------------------------------
SELECT pgivm.create_immv('gemini.script_records_immv', 'select * from gemini.script_records');

-------------------------------------------------------------------------------
-- Model Records IMMV
-------------------------------------------------------------------------------
SELECT pgivm.create_immv('gemini.model_records_immv', 'select * from gemini.model_records');

-------------------------------------------------------------------------------
-- Dataset Records IMMV
-------------------------------------------------------------------------------
SELECT pgivm.create_immv('gemini.dataset_records_immv', 'select * from gemini.dataset_records');


SET max_parallel_workers = DEFAULT;
SET default_table_access_method = 'heap';