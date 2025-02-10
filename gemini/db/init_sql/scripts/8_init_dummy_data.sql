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
    plot_id UUID;
    cultivar_id UUID;
BEGIN
    FOR plot_id IN SELECT id FROM gemini.plots LOOP
        SELECT DISTINCT ON (cultivar_id) cultivar_id INTO cultivar_id FROM gemini.plants WHERE plot_id = plot_id ORDER BY RANDOM() LIMIT 1;
        INSERT INTO gemini.plot_cultivars (plot_id, cultivar_id, info, created_at, updated_at)
        VALUES (plot_id, cultivar_id, '{"description": "Test association"}', NOW(), NOW());
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

-- Add Test Platforms
INSERT INTO gemini.sensor_platforms (sensor_platform_name, sensor_platform_info, created_at, updated_at)
VALUES
    ('Platform A', '{"description": "Test platform A"}', NOW(), NOW()),
    ('Platform B', '{"description": "Test platform B"}', NOW(), NOW()),
    ('Platform C', '{"description": "Test platform C"}', NOW(), NOW());


-- -------------------------------------------------------------------------------
-- -- Platforms Table
-- -- This is where all the platform information is stored
-- -- A platform is a collection of sensors

-- CREATE TABLE IF NOT EXISTS gemini.sensor_platforms (
--     id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
--     sensor_platform_name VARCHAR(255) NOT NULL,
--     sensor_platform_info JSONB DEFAULT '{}',
--     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
--     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );

-- CREATE INDEX IF NOT EXISTS idx_sensor_platforms_info ON gemini.sensor_platforms USING GIN (sensor_platform_info);

-- ALTER TABLE gemini.sensor_platforms ADD CONSTRAINT sensor_platform_unique UNIQUE NULLS NOT DISTINCT (sensor_platform_name);

-- -------------------------------------------------------------------------------
-- -- Sensors Table
-- -- This is where all the sensor information is stored
-- CREATE TABLE IF NOT EXISTS gemini.sensors (
--     id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
--     sensor_name VARCHAR(255) NOT NULL,
--     sensor_type_id INTEGER REFERENCES gemini.sensor_types(id) DEFAULT 0,
--     sensor_data_type_id INTEGER REFERENCES gemini.data_types(id) DEFAULT 0,
--     sensor_data_format_id INTEGER REFERENCES gemini.data_formats(id) DEFAULT 0,
--     sensor_info JSONB DEFAULT '{}',
--     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
--     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );

-- CREATE INDEX IF NOT EXISTS idx_sensors_info ON gemini.sensors USING GIN (sensor_info);

-- ALTER TABLE gemini.sensors ADD CONSTRAINT sensor_unique UNIQUE NULLS NOT DISTINCT (sensor_name);


-- -------------------------------------------------------------------------------
-- -- Resources Table
-- -- This is where all the resource information is stored, you can add a resource
-- CREATE TABLE IF NOT EXISTS gemini.resources (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     resource_uri VARCHAR(255),
--     resource_file_name VARCHAR(255),
--     is_external BOOLEAN DEFAULT FALSE,
--     resource_experiment_id UUID REFERENCES gemini.experiments(id) DEFAULT NULL,
--     resource_data_format_id INTEGER REFERENCES gemini.data_formats(id) DEFAULT 0,
--     resource_info JSONB DEFAULT '{}',
--     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
--     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );

-- CREATE INDEX IF NOT EXISTS idx_resources_info ON gemini.resources USING GIN (resource_info);

-- ALTER TABLE gemini.resources ADD CONSTRAINT resource_unique UNIQUE NULLS NOT DISTINCT (resource_uri, resource_file_name);

-- -------------------------------------------------------------------------------
-- -- Scripts Table
-- -- This is where all the script information is stored, you can add a script
-- CREATE TABLE IF NOT EXISTS gemini.scripts (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     script_name VARCHAR(255),
--     script_url VARCHAR(255),
--     script_extension VARCHAR(255),
--     script_info JSONB DEFAULT '{}',
--     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
--     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );

-- CREATE INDEX IF NOT EXISTS idx_scripts_info ON gemini.scripts USING GIN (script_info);

-- ALTER TABLE gemini.scripts ADD CONSTRAINT script_unique UNIQUE NULLS NOT DISTINCT (script_name, script_url);

-- -------------------------------------------------------------------------------
-- -- Script Runs Table
-- -- This is where all the script run information is stored, you can add a script run
-- CREATE TABLE IF NOT EXISTS gemini.script_runs (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     script_id UUID REFERENCES gemini.scripts(id) ON DELETE CASCADE,
--     script_run_info JSONB DEFAULT '{}',
--     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
--     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );

-- CREATE INDEX IF NOT EXISTS idx_script_runs_info ON gemini.script_runs USING GIN (script_run_info);

-- ALTER TABLE gemini.script_runs ADD CONSTRAINT script_run_unique UNIQUE NULLS NOT DISTINCT (script_id, script_run_info);

-- -------------------------------------------------------------------------------
-- -- Models Table
-- -- This is where all the model information is stored, you can add a model
-- CREATE TABLE IF NOT EXISTS gemini.models (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     model_name VARCHAR(255),
--     model_url VARCHAR(255),
--     model_info JSONB DEFAULT '{}',
--     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
--     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );

-- CREATE INDEX IF NOT EXISTS idx_models_info ON gemini.models USING GIN (model_info);

-- ALTER TABLE gemini.models ADD CONSTRAINT model_unique UNIQUE NULLS NOT DISTINCT (model_name, model_url);

-- -------------------------------------------------------------------------------
-- -- Model Runs Table
-- -- This is where all the model run information is stored, you can add a model run
-- CREATE TABLE IF NOT EXISTS gemini.model_runs (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     model_id UUID REFERENCES gemini.models(id) ON DELETE CASCADE,
--     model_run_info JSONB DEFAULT '{}',
--     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
--     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );

-- CREATE INDEX IF NOT EXISTS idx_model_runs_info ON gemini.model_runs USING GIN (model_run_info);

-- ALTER TABLE gemini.model_runs ADD CONSTRAINT model_run_unique UNIQUE NULLS NOT DISTINCT (model_id, model_run_info);

-- -------------------------------------------------------------------------------
-- -- Procedures Table
-- -- This is where all the procedure information is stored, you can add a procedure
-- CREATE TABLE IF NOT EXISTS gemini.procedures (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     procedure_name VARCHAR(255),
--     procedure_info JSONB DEFAULT '{}',
--     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
--     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );

-- CREATE INDEX IF NOT EXISTS idx_procedures_info ON gemini.procedures USING GIN (procedure_info);

-- ALTER TABLE gemini.procedures ADD CONSTRAINT procedure_unique UNIQUE NULLS NOT DISTINCT (procedure_name);

-- -------------------------------------------------------------------------------
-- -- Procedure Runs Table
-- -- This is where all the procedure run information is stored, you can add a procedure run
-- CREATE TABLE IF NOT EXISTS gemini.procedure_runs (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     procedure_id UUID REFERENCES gemini.procedures(id) ON DELETE CASCADE,
--     procedure_run_info JSONB DEFAULT '{}',
--     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
--     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );

-- CREATE INDEX IF NOT EXISTS idx_procedure_runs_info ON gemini.procedure_runs USING GIN (procedure_run_info);

-- ALTER TABLE gemini.procedure_runs ADD CONSTRAINT procedure_run_unique UNIQUE NULLS NOT DISTINCT (procedure_id, procedure_run_info);

-- -------------------------------------------------------------------------------
-- -- Dataset Types Table
-- -- This is where all the dataset type information is stored
-- CREATE TABLE IF NOT EXISTS gemini.dataset_types (
--     id INTEGER PRIMARY KEY,
--     dataset_type_name VARCHAR(255) NOT NULL,
--     dataset_type_info JSONB DEFAULT '{}',
--     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
--     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );

-- CREATE INDEX IF NOT EXISTS idx_dataset_types_info ON gemini.dataset_types USING GIN (dataset_type_info);

-- ALTER TABLE gemini.dataset_types ADD CONSTRAINT dataset_type_unique UNIQUE NULLS NOT DISTINCT (dataset_type_name);

-- -------------------------------------------------------------------------------
-- -- Datasets Table
-- -- This is where all the dataset information is stored
-- CREATE TABLE IF NOT EXISTS gemini.datasets(
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     collection_date DATE DEFAULT NOW(),
--     dataset_name VARCHAR(255),
--     dataset_info JSONB DEFAULT '{}',
--     dataset_type_id INTEGER REFERENCES gemini.dataset_types(id) DEFAULT 0,
--     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
--     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );

-- CREATE INDEX IF NOT EXISTS idx_datasets_info ON gemini.datasets USING GIN (dataset_info);

-- ALTER TABLE gemini.datasets ADD CONSTRAINT dataset_name_unique UNIQUE NULLS NOT DISTINCT (dataset_name);
