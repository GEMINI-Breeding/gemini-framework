-------------------------------------------------------------------------------
-- Table Definitions
-------------------------------------------------------------------------------

-- Experiments Table
-- Stores information about the experiments, including for GEMINI
CREATE TABLE IF NOT EXISTS gemini.experiments (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_name varchar(255) NOT NULL,
    experiment_info JSONB DEFAULT '{}',
    experiment_start_date DATE DEFAULT NOW(),
    experiment_end_date DATE, -- Value might be replaced by a trigger
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_experiments_info ON gemini.experiments USING GIN (experiment_info);

ALTER TABLE gemini.experiments ADD CONSTRAINT experiment_unique UNIQUE (experiment_name);
ALTER TABLE gemini.experiments ADD CONSTRAINT experiment_start_date_check CHECK (experiment_start_date <= experiment_end_date);
ALTER TABLE gemini.experiments ADD CONSTRAINT experiment_end_date_check CHECK (experiment_end_date >= experiment_start_date);

-------------------------------------------------------------------------------
-- Seasons Table
-- Each experiment can have multiple seasons
CREATE TABLE IF NOT EXISTS gemini.seasons (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id uuid REFERENCES gemini.experiments(id),
    season_name VARCHAR(255) NOT NULL,
    season_info JSONB DEFAULT '{}',
    season_start_date DATE DEFAULT NOW(),
    season_end_date DATE, -- Value might be replaced by a trigger
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_seasons_info ON gemini.seasons USING GIN (season_info);

ALTER TABLE gemini.seasons ADD CONSTRAINT season_unique UNIQUE (experiment_id, season_name);
ALTER TABLE gemini.seasons ADD CONSTRAINT season_start_date_check CHECK (season_start_date <= season_end_date);
ALTER TABLE gemini.seasons ADD CONSTRAINT season_end_date_check CHECK (season_end_date >= season_start_date);

-------------------------------------------------------------------------------
-- Sites Table
-- Each experiment can have multiple sites
CREATE TABLE IF NOT EXISTS gemini.sites (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    site_name varchar(255) NOT NULL,
    site_city varchar(255) DEFAULT '',
    site_state varchar(255) DEFAULT '',
    site_country varchar(255) DEFAULT '',
    site_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sites_info ON gemini.sites USING GIN (site_info);

ALTER TABLE gemini.sites ADD CONSTRAINT site_unique UNIQUE (site_name, site_city, site_state, site_country);

-------------------------------------------------------------------------------
-- Cultivars Table
-- Each experiment can have multiple cultivars, and they are a combination of accession and population
CREATE TABLE IF NOT EXISTS gemini.cultivars (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    cultivar_accession VARCHAR(255) NOT NULL,
    cultivar_population VARCHAR(255) NOT NULL,
    cultivar_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cultivars_info ON gemini.cultivars USING GIN (cultivar_info);

ALTER TABLE gemini.cultivars ADD CONSTRAINT cultivar_unique UNIQUE (cultivar_accession, cultivar_population);

-------------------------------------------------------------------------------
-- Plots Table
-- This is where all the plot information is stored
CREATE TABLE IF NOT EXISTS gemini.plots (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id uuid REFERENCES gemini.experiments(id),
    season_id uuid REFERENCES gemini.seasons(id),
    site_id uuid REFERENCES gemini.sites(id),
    plot_number INTEGER,
    plot_row_number INTEGER,
    plot_column_number INTEGER,
    plot_geometry_info JSONB DEFAULT '{}',
    plot_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
    

CREATE INDEX IF NOT EXISTS idx_plots_info ON gemini.plots USING GIN (plot_info);

ALTER TABLE gemini.plots ADD CONSTRAINT plot_unique UNIQUE (experiment_id, season_id, site_id, plot_number, plot_row_number, plot_column_number);

-------------------------------------------------------------------------------
-- Plants Table
-- This is where all the plant information is stored
CREATE TABLE IF NOT EXISTS gemini.plants (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    plot_id uuid REFERENCES gemini.plots(id),
    plant_number INTEGER,
    plant_info JSONB DEFAULT '{}',
    cultivar_id uuid REFERENCES gemini.cultivars(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_plants_info ON gemini.plants USING GIN (plant_info);

ALTER TABLE gemini.plants ADD CONSTRAINT plant_unique UNIQUE (plot_id, plant_number);


-------------------------------------------------------------------------------
-- Data Types Table
-- This is where we will store all possible Data Types that are compatible with GEMINI
-- Acts like a global enumeration for data types
CREATE TABLE IF NOT EXISTS gemini.data_types (
    id INTEGER PRIMARY KEY,
    data_type_name VARCHAR(255) NOT NULL,
    data_type_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_data_types_info ON gemini.data_types USING GIN (data_type_info);

ALTER TABLE gemini.data_types ADD CONSTRAINT data_type_unique UNIQUE NULLS NOT DISTINCT (data_type_name);

-------------------------------------------------------------------------------
-- Data Formats Table
-- This is where we will store all possible Data Formats that are compatible with GEMINI
-- Stores File Formats
CREATE TABLE IF NOT EXISTS gemini.data_formats (
    id INTEGER PRIMARY KEY,
    data_format_name VARCHAR(255) NOT NULL,
    data_format_mime_type VARCHAR(255) DEFAULT 'application/octet-stream',
    data_format_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_data_formats_info ON gemini.data_formats USING GIN (data_format_info);

ALTER TABLE gemini.data_formats ADD CONSTRAINT data_format_unique UNIQUE NULLS NOT DISTINCT (data_format_name);

-------------------------------------------------------------------------------
-- Trait Levels Table
-- This is where we will store all possible Trait Levels that are compatible with GEMINI
-- Acts like a global enumeration for trait levels
CREATE TABLE IF NOT EXISTS gemini.trait_levels (
    id INTEGER PRIMARY KEY,
    trait_level_name VARCHAR(255) NOT NULL,
    trait_level_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_trait_levels_info ON gemini.trait_levels USING GIN (trait_level_info);

ALTER TABLE gemini.trait_levels ADD CONSTRAINT trait_level_unique UNIQUE NULLS NOT DISTINCT (trait_level_name);

-------------------------------------------------------------------------------
-- Traits Table
-- This is where all the trait information is stored
CREATE TABLE IF NOT EXISTS gemini.traits (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    trait_name VARCHAR(255) NOT NULL,
    trait_units VARCHAR(255) DEFAULT 'units',
    trait_level_id INTEGER REFERENCES gemini.trait_levels(id) DEFAULT 0,
    trait_metrics JSONB DEFAULT '{}',
    trait_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE INDEX IF NOT EXISTS idx_traits_info ON gemini.traits USING GIN (trait_info);

ALTER TABLE gemini.traits ADD CONSTRAINT trait_unique UNIQUE NULLS NOT DISTINCT (trait_name);

-------------------------------------------------------------------------------
-- Sensor Types Table
-- This is where we will store all possible Sensor Types that are compatible with GEMINI
-- Acts like a global enumeration for sensor types
CREATE TABLE IF NOT EXISTS gemini.sensor_types (
    id INTEGER PRIMARY KEY,
    sensor_type_name VARCHAR(255) NOT NULL,
    sensor_type_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sensor_types_info ON gemini.sensor_types USING GIN (sensor_type_info);

ALTER TABLE gemini.sensor_types ADD CONSTRAINT sensor_type_unique UNIQUE NULLS NOT DISTINCT (sensor_type_name);

-------------------------------------------------------------------------------
-- Platforms Table
-- This is where all the platform information is stored
-- A platform is a collection of sensors

CREATE TABLE IF NOT EXISTS gemini.sensor_platforms (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    sensor_platform_name VARCHAR(255) NOT NULL,
    sensor_platform_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sensor_platforms_info ON gemini.sensor_platforms USING GIN (sensor_platform_info);

ALTER TABLE gemini.sensor_platforms ADD CONSTRAINT sensor_platform_unique UNIQUE NULLS NOT DISTINCT (sensor_platform_name);

-------------------------------------------------------------------------------
-- Sensors Table
-- This is where all the sensor information is stored
CREATE TABLE IF NOT EXISTS gemini.sensors (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    sensor_name VARCHAR(255) NOT NULL,
    sensor_type_id INTEGER REFERENCES gemini.sensor_types(id) DEFAULT 0,
    sensor_data_type_id INTEGER REFERENCES gemini.data_types(id) DEFAULT 0,
    sensor_data_format_id INTEGER REFERENCES gemini.data_formats(id) DEFAULT 0,
    sensor_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sensors_info ON gemini.sensors USING GIN (sensor_info);

ALTER TABLE gemini.sensors ADD CONSTRAINT sensor_unique UNIQUE NULLS NOT DISTINCT (sensor_name);


-------------------------------------------------------------------------------
-- Resources Table
-- This is where all the resource information is stored, you can add a resource
CREATE TABLE IF NOT EXISTS gemini.resources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    resource_uri VARCHAR(255),
    resource_file_name VARCHAR(255),
    is_external BOOLEAN DEFAULT FALSE,
    resource_experiment_id UUID REFERENCES gemini.experiments(id) DEFAULT NULL,
    resource_data_format_id INTEGER REFERENCES gemini.data_formats(id) DEFAULT 0,
    resource_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_resources_info ON gemini.resources USING GIN (resource_info);

ALTER TABLE gemini.resources ADD CONSTRAINT resource_unique UNIQUE NULLS NOT DISTINCT (resource_uri, resource_file_name);

-------------------------------------------------------------------------------
-- Scripts Table
-- This is where all the script information is stored, you can add a script
CREATE TABLE IF NOT EXISTS gemini.scripts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    script_name VARCHAR(255),
    script_url VARCHAR(255),
    script_extension VARCHAR(255),
    script_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_scripts_info ON gemini.scripts USING GIN (script_info);

ALTER TABLE gemini.scripts ADD CONSTRAINT script_unique UNIQUE NULLS NOT DISTINCT (script_name, script_url);

-------------------------------------------------------------------------------
-- Script Runs Table
-- This is where all the script run information is stored, you can add a script run
CREATE TABLE IF NOT EXISTS gemini.script_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    script_id UUID REFERENCES gemini.scripts(id) ON DELETE CASCADE,
    script_run_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_script_runs_info ON gemini.script_runs USING GIN (script_run_info);

ALTER TABLE gemini.script_runs ADD CONSTRAINT script_run_unique UNIQUE NULLS NOT DISTINCT (script_id, script_run_info);

-------------------------------------------------------------------------------
-- Models Table
-- This is where all the model information is stored, you can add a model
CREATE TABLE IF NOT EXISTS gemini.models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_name VARCHAR(255),
    model_url VARCHAR(255),
    model_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_models_info ON gemini.models USING GIN (model_info);

ALTER TABLE gemini.models ADD CONSTRAINT model_unique UNIQUE NULLS NOT DISTINCT (model_name, model_url);

-------------------------------------------------------------------------------
-- Model Runs Table
-- This is where all the model run information is stored, you can add a model run
CREATE TABLE IF NOT EXISTS gemini.model_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_id UUID REFERENCES gemini.models(id) ON DELETE CASCADE,
    model_run_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_model_runs_info ON gemini.model_runs USING GIN (model_run_info);

ALTER TABLE gemini.model_runs ADD CONSTRAINT model_run_unique UNIQUE NULLS NOT DISTINCT (model_id, model_run_info);

-------------------------------------------------------------------------------
-- Procedures Table
-- This is where all the procedure information is stored, you can add a procedure
CREATE TABLE IF NOT EXISTS gemini.procedures (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    procedure_name VARCHAR(255),
    procedure_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_procedures_info ON gemini.procedures USING GIN (procedure_info);

ALTER TABLE gemini.procedures ADD CONSTRAINT procedure_unique UNIQUE NULLS NOT DISTINCT (procedure_name);

-------------------------------------------------------------------------------
-- Procedure Runs Table
-- This is where all the procedure run information is stored, you can add a procedure run
CREATE TABLE IF NOT EXISTS gemini.procedure_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    procedure_id UUID REFERENCES gemini.procedures(id) ON DELETE CASCADE,
    procedure_run_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_procedure_runs_info ON gemini.procedure_runs USING GIN (procedure_run_info);

ALTER TABLE gemini.procedure_runs ADD CONSTRAINT procedure_run_unique UNIQUE NULLS NOT DISTINCT (procedure_id, procedure_run_info);

-------------------------------------------------------------------------------
-- Dataset Types Table
-- This is where all the dataset type information is stored
CREATE TABLE IF NOT EXISTS gemini.dataset_types (
    id INTEGER PRIMARY KEY,
    dataset_type_name VARCHAR(255) NOT NULL,
    dataset_type_info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_dataset_types_info ON gemini.dataset_types USING GIN (dataset_type_info);

ALTER TABLE gemini.dataset_types ADD CONSTRAINT dataset_type_unique UNIQUE NULLS NOT DISTINCT (dataset_type_name);

-------------------------------------------------------------------------------
-- Datasets Table
-- This is where all the dataset information is stored
CREATE TABLE IF NOT EXISTS gemini.datasets(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    collection_date DATE DEFAULT NOW(),
    dataset_name VARCHAR(255),
    dataset_info JSONB DEFAULT '{}',
    dataset_type_id INTEGER REFERENCES gemini.dataset_types(id) DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_datasets_info ON gemini.datasets USING GIN (dataset_info);

ALTER TABLE gemini.datasets ADD CONSTRAINT dataset_name_unique UNIQUE NULLS NOT DISTINCT (dataset_name);


