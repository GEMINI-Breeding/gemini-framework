-------------------------------------------------------------------------------
-- Dummy data for testing
-------------------------------------------------------------------------------

-- Add Dummy Experiment Data
INSERT INTO gemini.experiments (experiment_name, experiment_info, experiment_start_date, experiment_end_date, created_at, updated_at)
VALUES 
    ('Experiment A', '{"description": "Test experiment A"}', '2023-01-01', '2023-12-31', NOW(), NOW()),
    ('Experiment B', '{"description": "Test experiment B"}', '2024-01-01', '2024-12-31', NOW(), NOW());


-- Add 3 Dummy Seasons per Experiment
INSERT INTO gemini.seasons (experiment_id, season_name, season_info, season_start_date, season_end_date, created_at, updated_at)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), 'Season 1', '{"description": "Test season 1"}', '2023-01-01', '2023-03-31', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), 'Season 2', '{"description": "Test season 2"}', '2023-04-01', '2023-09-30', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), 'Season 3', '{"description": "Test season 3"}', '2023-10-01', '2023-12-31', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), 'Season 1', '{"description": "Test season 1"}', '2024-01-01', '2024-03-31', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), 'Season 2', '{"description": "Test season 2"}', '2024-04-01', '2024-09-30', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), 'Season 3', '{"description": "Test season 3"}', '2024-10-01', '2024-12-31', NOW(), NOW());

-- Add 3 Dummy Sites
INSERT INTO gemini.sites (site_name, site_city, site_state, site_country, site_info, created_at, updated_at)
VALUES
    ('Site A', 'City A', 'State A', 'Country A', '{"description": "Test site A"}', NOW(), NOW()),
    ('Site B', 'City B', 'State B', 'Country B', '{"description": "Test site B"}', NOW(), NOW()),
    ('Site C', 'City C', 'State C', 'Country C', '{"description": "Test site C"}', NOW(), NOW());


-- Add associations to experiment_sites
INSERT INTO gemini.experiment_sites (experiment_id, site_id, info, created_at, updated_at)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.sites WHERE site_name = 'Site A' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.sites WHERE site_name = 'Site B' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.sites WHERE site_name = 'Site C' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.sites WHERE site_name = 'Site A' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.sites WHERE site_name = 'Site B' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.sites WHERE site_name = 'Site C' LIMIT 1), '{"description": "Test association"}', NOW(), NOW());


-- Add 12 Cultivars, 3 for each dummy population
INSERT INTO gemini.cultivars (cultivar_accession, cultivar_population, cultivar_info, created_at, updated_at)
VALUES
    ('Accession A1', 'Population A', '{"description": "Test cultivar A1"}', NOW(), NOW()),
    ('Accession A2', 'Population A', '{"description": "Test cultivar A2"}', NOW(), NOW()),
    ('Accession A3', 'Population A', '{"description": "Test cultivar A3"}', NOW(), NOW()),
    ('Accession B1', 'Population B', '{"description": "Test cultivar B1"}', NOW(), NOW()),
    ('Accession B2', 'Population B', '{"description": "Test cultivar B2"}', NOW(), NOW()),
    ('Accession B3', 'Population B', '{"description": "Test cultivar B3"}', NOW(), NOW()),
    ('Accession C1', 'Population C', '{"description": "Test cultivar C1"}', NOW(), NOW()),
    ('Accession C2', 'Population C', '{"description": "Test cultivar C2"}', NOW(), NOW()),
    ('Accession C3', 'Population C', '{"description": "Test cultivar C3"}', NOW(), NOW());

-- Add associations to experiment_cultivars
INSERT INTO gemini.experiment_cultivars (experiment_id, cultivar_id, info, created_at, updated_at)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.cultivars WHERE cultivar_accession = 'Accession A1' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.cultivars WHERE cultivar_accession = 'Accession A2' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.cultivars WHERE cultivar_accession = 'Accession A3' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.cultivars WHERE cultivar_accession = 'Accession B1' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.cultivars WHERE cultivar_accession = 'Accession B2' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.cultivars WHERE cultivar_accession = 'Accession B3' LIMIT 1), '{"description": "Test association"}', NOW(), NOW());


-- For each combination of experiment, season, and site, add 20 plots
-- Use an anonymous function to generate plot numbers
DO $$
DECLARE
    exp_id UUID;
    season_id UUID;
    site_id UUID;
    plot_number INTEGER;
    plot_row_number INTEGER;
    plot_column_number INTEGER;
    plot_info JSONB;
BEGIN
    FOR exp_id IN SELECT id FROM gemini.experiments LOOP
        FOR season_id IN SELECT id FROM gemini.seasons WHERE experiment_id = exp_id LOOP
            FOR site_id IN SELECT id FROM gemini.sites LOOP
                FOR plot_number IN 1..20 LOOP
                    plot_row_number := (plot_number - 1) / 5 + 1;
                    plot_column_number := (plot_number - 1) % 5 + 1;
                    plot_info := jsonb_build_object('description', 'Test plot ' || plot_number);
                    INSERT INTO gemini.plots (experiment_id, season_id, site_id, plot_number, plot_row_number, plot_column_number, plot_info, created_at, updated_at)
                    VALUES (exp_id, season_id, site_id, plot_number, plot_row_number, plot_column_number, plot_info, NOW(), NOW());
                END LOOP;
            END LOOP;
        END LOOP;
    END LOOP;
END $$;


-- For each plot, add 2 plants of random cultivars, but each plot can only have one kind of cultivar
DO $$
DECLARE
    plot_id UUID;
    cultivar_id UUID;
    plant_number INTEGER;
BEGIN
    FOR plot_id IN SELECT id FROM gemini.plots LOOP
        -- Select a random cultivar from the cultivars table
        SELECT id INTO cultivar_id FROM gemini.cultivars ORDER BY RANDOM() LIMIT 1;
        -- Insert 2 plants for each plot with the same cultivar
        FOR plant_number IN 1..2 LOOP
            INSERT INTO gemini.plants (plot_id, plant_number, plant_info, cultivar_id, created_at, updated_at)
            VALUES (plot_id, plant_number, jsonb_build_object('description', 'Test plant ' || plant_number), cultivar_id, NOW(), NOW());
        END LOOP;
    END LOOP;
END $$;

-- Add associations to plot_cultivars based on plants table
DO $$
DECLARE
    plot_uuid UUID;
    cultivar_id UUID;
BEGIN
    FOR plot_uuid IN (SELECT id FROM gemini.plots) LOOP
        -- Select the unique cultivar_id from plants within the plot
        SELECT DISTINCT p.cultivar_id 
        INTO cultivar_id 
        FROM gemini.plants p 
        WHERE p.plot_id = plot_uuid;

        -- Only insert if there is a valid cultivar associated with the plot
        IF cultivar_id IS NOT NULL THEN
            INSERT INTO gemini.plot_cultivars (plot_id, cultivar_id, info, created_at, updated_at)
            VALUES (plot_uuid, cultivar_id, '{"description": "Verified association"}', NOW(), NOW());
        END IF;
    END LOOP;
END $$;

-- Add 6 Dummy Traits
INSERT INTO gemini.traits (trait_name, trait_units, trait_level_id, trait_metrics, trait_info, created_at, updated_at)
VALUES
    ('Trait A', 'g/m2', 1, '{"mean": 10, "std_dev": 2}', '{"description": "Test trait A"}', NOW(), NOW()),
    ('Trait B', 'g/m2', 2, '{"mean": 15, "std_dev": 3}', '{"description": "Test trait B"}', NOW(), NOW()),
    ('Trait C', 'g/m2', 1, '{"mean": 20, "std_dev": 4}', '{"description": "Test trait C"}', NOW(), NOW()),
    ('Trait D', 'g/m2', 2, '{"mean": 25, "std_dev": 5}', '{"description": "Test trait D"}', NOW(), NOW()),
    ('Trait E', 'g/m2', 1, '{"mean": 30, "std_dev": 6}', '{"description": "Test trait E"}', NOW(), NOW()),
    ('Trait F', 'g/m2', 2, '{"mean": 35, "std_dev": 7}', '{"description": "Test trait F"}', NOW(), NOW());

-- Add associations to experiment_traits, 3 traits exclusively per experiment
-- Add A,B,C to Experiment A, D,E,F to Experiment B
INSERT INTO gemini.experiment_traits (experiment_id, trait_id, info, created_at, updated_at)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.traits WHERE trait_name = 'Trait A' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.traits WHERE trait_name = 'Trait B' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.traits WHERE trait_name = 'Trait C' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.traits WHERE trait_name = 'Trait D' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.traits WHERE trait_name = 'Trait E' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.traits WHERE trait_name = 'Trait F' LIMIT 1), '{"description": "Test association"}', NOW(), NOW());


-- Add Dummy Platforms
INSERT INTO gemini.sensor_platforms (sensor_platform_name, sensor_platform_info, created_at, updated_at)
VALUES
    ('Platform A', '{"description": "Test platform A"}', NOW(), NOW()),
    ('Platform B', '{"description": "Test platform B"}', NOW(), NOW()),
    ('Platform C', '{"description": "Test platform C"}', NOW(), NOW());


-- Create 8 Dummy Sensors of assorted type, data type, and data format
INSERT INTO gemini.sensors (sensor_name, sensor_type_id, sensor_data_type_id, sensor_data_format_id, sensor_info, created_at, updated_at)
VALUES
    ('Sensor A1', 1, 1, 1, '{"description": "Test sensor A1"}', NOW(), NOW()),
    ('Sensor A2', 1, 1, 1, '{"description": "Test sensor A2"}', NOW(), NOW()),
    ('Sensor A3', 1, 1, 1, '{"description": "Test sensor A3"}', NOW(), NOW()),
    ('Sensor B1', 1, 1, 1, '{"description": "Test sensor B1"}', NOW(), NOW()),
    ('Sensor B2', 1, 1, 1, '{"description": "Test sensor B2"}', NOW(), NOW()),
    ('Sensor B3', 1, 1, 1, '{"description": "Test sensor B3"}', NOW(), NOW()),
    ('Sensor C1', 1, 1, 1, '{"description": "Test sensor C1"}', NOW(), NOW()),
    ('Sensor C2', 1, 1, 1, '{"description": "Test sensor C2"}', NOW(), NOW());

-- For platform A, add sensors A1, A2, A3
-- For platform B, add sensors B1, B2, B3
-- For platform C, add sensors C1, C2
INSERT INTO gemini.sensor_platform_sensors (sensor_platform_id, sensor_id, info, created_at, updated_at)
VALUES
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Platform A' LIMIT 1), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Sensor A1' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Platform A' LIMIT 1), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Sensor A2' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Platform A' LIMIT 1), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Sensor A3' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Platform B' LIMIT 1), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Sensor B1' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Platform B' LIMIT 1), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Sensor B2' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Platform B' LIMIT 1), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Sensor B3' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Platform C' LIMIT 1), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Sensor C1' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Platform C' LIMIT 1), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Sensor C2' LIMIT 1), '{"description": "Test association"}', NOW(), NOW());


-- Add Platforms to Experiments
INSERT INTO gemini.experiment_sensor_platforms (experiment_id, sensor_platform_id, info, created_at, updated_at)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Platform A' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Platform B' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Platform B' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Platform C' LIMIT 1), '{"description": "Test association"}', NOW(), NOW());

-- Add Sensors to Experiments
INSERT INTO gemini.experiment_sensors (experiment_id, sensor_id, info, created_at, updated_at)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Sensor A1' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Sensor A2' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Sensor A3' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Sensor B1' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Sensor B2' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Sensor B3' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Sensor C1' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Sensor C2' LIMIT 1), '{"description": "Test association"}', NOW(), NOW());


-- Add 2 internal and 3 external resources (External resources have actual links that work)
INSERT INTO gemini.resources (resource_uri, resource_file_name, is_external, resource_experiment_id, resource_data_format_id, resource_info, created_at, updated_at)
VALUES
    ('/path/to/internal/resource1', 'internal_resource1.txt', FALSE, (SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), 1, '{"description": "Test internal resource 1"}', NOW(), NOW()),
    ('/path/to/internal/resource2', 'internal_resource2.txt', FALSE, (SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), 1, '{"description": "Test internal resource 2"}', NOW(), NOW()),
    ('https://www.google.com', 'external_resource1.txt', TRUE, (SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), 1, '{"description": "Test external resource 1"}', NOW(), NOW()),
    ('https://www.yahoo.com', 'external_resource2.txt', TRUE, (SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), 1, '{"description": "Test external resource 2"}', NOW(), NOW()),
    ('https://www.bing.com', 'external_resource3.txt', TRUE, (SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), 1, '{"description": "Test external resource 3"}', NOW(), NOW());


-- Add 3 Dummy Scripts
INSERT INTO gemini.scripts (script_name, script_url, script_extension, script_info, created_at, updated_at)
VALUES
    ('Script A', '/path/to/scriptA', 'py', '{"description": "Test script A"}', NOW(), NOW()),
    ('Script B', '/path/to/scriptB', 'py', '{"description": "Test script B"}', NOW(), NOW()),
    ('Script C', '/path/to/scriptC', 'py', '{"description": "Test script C"}', NOW(), NOW());

-- Randomly assign scripts to experiments
INSERT INTO gemini.experiment_scripts (experiment_id, script_id, info, created_at, updated_at)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.scripts WHERE script_name = 'Script A' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.scripts WHERE script_name = 'Script B' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.scripts WHERE script_name = 'Script B' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.scripts WHERE script_name = 'Script C' LIMIT 1), '{"description": "Test association"}', NOW(), NOW());

-- Create at most 30 random script runs for each script
DO $$
DECLARE
    script_uuid UUID;
    script_run_info JSONB;
    script_run_count INTEGER;
BEGIN
    FOR script_uuid IN SELECT id FROM gemini.scripts LOOP
        script_run_count := 1 + (random() * 30)::INTEGER;
        FOR i IN 1..script_run_count LOOP
            script_run_info := jsonb_build_object('run_number', i, 'run_info', 'Test run ' || i);
            INSERT INTO gemini.script_runs (script_id, script_run_info, created_at, updated_at)
            VALUES (script_uuid, script_run_info, NOW(), NOW());
        END LOOP;
    END LOOP;
END $$;

-- Add 3 Dummy Models
INSERT INTO gemini.models (model_name, model_url, model_info, created_at, updated_at)
VALUES
    ('Model A', '/path/to/modelA', '{"description": "Test model A"}', NOW(), NOW()),
    ('Model B', '/path/to/modelB', '{"description": "Test model B"}', NOW(), NOW()),
    ('Model C', '/path/to/modelC', '{"description": "Test model C"}', NOW(), NOW());

-- Randomly assign models to experiments
INSERT INTO gemini.experiment_models (experiment_id, model_id, info, created_at, updated_at)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.models WHERE model_name = 'Model A' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.models WHERE model_name = 'Model B' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.models WHERE model_name = 'Model B' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.models WHERE model_name = 'Model C' LIMIT 1), '{"description": "Test association"}', NOW(), NOW());

-- Create at most 30 random model runs for each model
DO $$
DECLARE
    model_id UUID;
    model_run_info JSONB;
    model_run_count INTEGER;
BEGIN
    FOR model_id IN SELECT id FROM gemini.models LOOP
        model_run_count := 1 + (random() * 30)::INTEGER;
        FOR i IN 1..model_run_count LOOP
            model_run_info := jsonb_build_object('run_number', i, 'run_info', 'Test run ' || i);
            INSERT INTO gemini.model_runs (model_id, model_run_info, created_at, updated_at)
            VALUES (model_id, model_run_info, NOW(), NOW());
        END LOOP;
    END LOOP;
END $$;

-- Add 3 Dummy Procedures
INSERT INTO gemini.procedures (procedure_name, procedure_info, created_at, updated_at)
VALUES
    ('Procedure A', '{"description": "Test procedure A"}', NOW(), NOW()),
    ('Procedure B', '{"description": "Test procedure B"}', NOW(), NOW()),
    ('Procedure C', '{"description": "Test procedure C"}', NOW(), NOW());

-- Randomly assign procedures to experiments
INSERT INTO gemini.experiment_procedures (experiment_id, procedure_id, info, created_at, updated_at)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.procedures WHERE procedure_name = 'Procedure A' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment A' LIMIT 1), (SELECT id FROM gemini.procedures WHERE procedure_name = 'Procedure B' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.procedures WHERE procedure_name = 'Procedure B' LIMIT 1), '{"description": "Test association"}', NOW(), NOW()),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Experiment B' LIMIT 1), (SELECT id FROM gemini.procedures WHERE procedure_name = 'Procedure C' LIMIT 1), '{"description": "Test association"}', NOW(), NOW());

-- Create at most 30 random procedure runs for each procedure
DO $$
DECLARE
    procedure_id UUID;
    procedure_run_info JSONB;
    procedure_run_count INTEGER;
BEGIN
    FOR procedure_id IN SELECT id FROM gemini.procedures LOOP
        procedure_run_count := 1 + (random() * 30)::INTEGER;
        FOR i IN 1..procedure_run_count LOOP
            procedure_run_info := jsonb_build_object('run_number', i, 'run_info', 'Test run ' || i);
            INSERT INTO gemini.procedure_runs (procedure_id, procedure_run_info, created_at, updated_at)
            VALUES (procedure_id, procedure_run_info, NOW(), NOW());
        END LOOP;
    END LOOP;
END $$;

-- Add 3 Datasets of Default Dataset Type
INSERT INTO gemini.datasets (dataset_name, dataset_type_id, dataset_info, created_at, updated_at)
VALUES
    ('Dataset A', 0, '{"description": "Test dataset A"}', NOW(), NOW()),
    ('Dataset B', 0, '{"description": "Test dataset B"}', NOW(), NOW()),
    ('Dataset C', 0, '{"description": "Test dataset C"}', NOW(), NOW());


-- For each sensor create 2 datasets of appropriate dataset type
DO $$
DECLARE
    s_name TEXT;
    dataset_name TEXT;
    dataset_info JSONB;
BEGIN
    FOR s_name IN SELECT sensor_name FROM gemini.sensors LOOP
        dataset_info := jsonb_build_object('description', 'Test dataset A for sensor ' || s_name);
        dataset_name := 'Dataset A for Sensor ' || s_name;
        INSERT INTO gemini.datasets (dataset_name, dataset_type_id, dataset_info, created_at, updated_at)
        VALUES (dataset_name, 1, dataset_info, NOW(), NOW());
        dataset_info := jsonb_build_object('description', 'Test dataset B for sensor ' || s_name);
        dataset_name := 'Dataset B for Sensor ' || s_name;
        INSERT INTO gemini.datasets (dataset_name, dataset_type_id, dataset_info, created_at, updated_at)
        VALUES (dataset_name, 1, dataset_info, NOW(), NOW());
    END LOOP;
END $$;

-- For each trait create 2 datasets of appropriate dataset type
DO $$
DECLARE
    t_name TEXT;
    dataset_name TEXT;
    dataset_info JSONB;
BEGIN
    FOR t_name IN SELECT trait_name FROM gemini.traits LOOP
        dataset_info := jsonb_build_object('description', 'Test dataset A for trait ' || t_name);
        dataset_name := 'Dataset A for Trait ' || t_name;
        INSERT INTO gemini.datasets (dataset_name, dataset_type_id, dataset_info, created_at, updated_at)
        VALUES (dataset_name, 2, dataset_info, NOW(), NOW());
        dataset_info := jsonb_build_object('description', 'Test dataset B for trait ' || t_name);
        dataset_name := 'Dataset B for Trait ' || t_name;
        INSERT INTO gemini.datasets (dataset_name, dataset_type_id, dataset_info, created_at, updated_at)
        VALUES (dataset_name, 2, dataset_info, NOW(), NOW());
    END LOOP;
END $$;

-- For each model create 2 datasets of appropriate dataset type
DO $$
DECLARE
    m_name TEXT;
    dataset_name TEXT;
    dataset_info JSONB;
BEGIN
    FOR m_name IN SELECT model_name FROM gemini.models LOOP
        dataset_info := jsonb_build_object('description', 'Test dataset A for model ' || m_name);
        dataset_name := 'Dataset A for Model ' || m_name;
        INSERT INTO gemini.datasets (dataset_name, dataset_type_id, dataset_info, created_at, updated_at)
        VALUES (dataset_name, 5, dataset_info, NOW(), NOW());
        dataset_info := jsonb_build_object('description', 'Test dataset B for model ' || m_name);
        dataset_name := 'Dataset B for Model ' || m_name;
        INSERT INTO gemini.datasets (dataset_name, dataset_type_id, dataset_info, created_at, updated_at)
        VALUES (dataset_name, 5, dataset_info, NOW(), NOW());
    END LOOP;
END $$;

-- For each procedure create 2 datasets of appropriate dataset type
DO $$
DECLARE
    p_name TEXT;
    dataset_name TEXT;
    dataset_info JSONB;
BEGIN
    FOR p_name IN SELECT procedure_name FROM gemini.procedures LOOP
        dataset_info := jsonb_build_object('description', 'Test dataset A for procedure ' || p_name);
        dataset_name := 'Dataset A for Procedure ' || p_name;
        INSERT INTO gemini.datasets (dataset_name, dataset_type_id, dataset_info, created_at, updated_at)
        VALUES (dataset_name, 3, dataset_info, NOW(), NOW());
        dataset_info := jsonb_build_object('description', 'Test dataset B for procedure ' || p_name);
        dataset_name := 'Dataset B for Procedure ' || p_name;
        INSERT INTO gemini.datasets (dataset_name, dataset_type_id, dataset_info, created_at, updated_at)
        VALUES (dataset_name, 3, dataset_info, NOW(), NOW());
    END LOOP;
END $$;

-- For each script create 2 datasets of appropriate dataset type
DO $$
DECLARE
    s_name TEXT;
    dataset_name TEXT;
    dataset_info JSONB;
BEGIN
    FOR s_name IN SELECT script_name FROM gemini.scripts LOOP
        dataset_info := jsonb_build_object('description', 'Test dataset A for script ' || s_name);
        dataset_name := 'Dataset A for Script ' || s_name;
        INSERT INTO gemini.datasets (dataset_name, dataset_type_id, dataset_info, created_at, updated_at)
        VALUES (dataset_name, 4, dataset_info, NOW(), NOW());
        dataset_info := jsonb_build_object('description', 'Test dataset B for script ' || s_name);
        dataset_name := 'Dataset B for Script ' || s_name;
        INSERT INTO gemini.datasets (dataset_name, dataset_type_id, dataset_info, created_at, updated_at)
        VALUES (dataset_name, 4, dataset_info, NOW(), NOW());
    END LOOP;
END $$;


