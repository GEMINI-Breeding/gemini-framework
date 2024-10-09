-------------------------------------------------------------------------------
-- Relationships
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
-- DataType Formats Table
-- This is where all the data type format information is stored
-- Each data type can have multiple formats
CREATE TABLE IF NOT EXISTS gemini.data_type_formats (
    data_type_id INTEGER REFERENCES gemini.data_types(id) ON DELETE CASCADE,
    data_format_id INTEGER REFERENCES gemini.data_formats(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (data_type_id, data_format_id)
);

-------------------------------------------------------------------------------
-- Experiment Sites Table

CREATE TABLE IF NOT EXISTS gemini.experiment_sites (
    experiment_id UUID REFERENCES gemini.experiments(id) ON DELETE CASCADE,
    site_id UUID REFERENCES gemini.sites(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (experiment_id, site_id)
);

-------------------------------------------------------------------------------
-- Experiment Sensors Table

CREATE TABLE IF NOT EXISTS gemini.experiment_sensors (
    experiment_id UUID REFERENCES gemini.experiments(id) ON DELETE CASCADE,
    sensor_id UUID REFERENCES gemini.sensors(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (experiment_id, sensor_id)
);

-------------------------------------------------------------------------------
-- Experiment Sensor Platforms Table

CREATE TABLE IF NOT EXISTS gemini.experiment_sensor_platforms (
    experiment_id UUID REFERENCES gemini.experiments(id) ON DELETE CASCADE,
    sensor_platform_id UUID REFERENCES gemini.sensor_platforms(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (experiment_id, sensor_platform_id)
);


-------------------------------------------------------------------------------
-- Experiment Traits Table

CREATE TABLE IF NOT EXISTS gemini.experiment_traits (
    experiment_id UUID REFERENCES gemini.experiments(id) ON DELETE CASCADE,
    trait_id UUID REFERENCES gemini.traits(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (experiment_id, trait_id)
);

-------------------------------------------------------------------------------
-- Experiment Cultivars Table

CREATE TABLE IF NOT EXISTS gemini.experiment_cultivars (
    experiment_id UUID REFERENCES gemini.experiments(id) ON DELETE CASCADE,
    cultivar_id UUID REFERENCES gemini.cultivars(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (experiment_id, cultivar_id)
);


-------------------------------------------------------------------------------
-- Experiment Datasets Table

CREATE TABLE IF NOT EXISTS gemini.experiment_datasets (
    experiment_id UUID REFERENCES gemini.experiments(id) ON DELETE CASCADE,
    dataset_id UUID REFERENCES gemini.datasets(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (experiment_id, dataset_id)
);

-------------------------------------------------------------------------------
-- Experiment Models Table

CREATE TABLE IF NOT EXISTS gemini.experiment_models (
    experiment_id UUID REFERENCES gemini.experiments(id) ON DELETE CASCADE,
    model_id UUID REFERENCES gemini.models(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (experiment_id, model_id)
);

-------------------------------------------------------------------------------
-- Experiment Procedures Table

CREATE TABLE IF NOT EXISTS gemini.experiment_procedures (
    experiment_id UUID REFERENCES gemini.experiments(id) ON DELETE CASCADE,
    procedure_id UUID REFERENCES gemini.procedures(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (experiment_id, procedure_id)
);

-------------------------------------------------------------------------------
-- Experiment Scripts Table

CREATE TABLE IF NOT EXISTS gemini.experiment_scripts (
    experiment_id UUID REFERENCES gemini.experiments(id) ON DELETE CASCADE,
    script_id UUID REFERENCES gemini.scripts(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (experiment_id, script_id)
);

-------------------------------------------------------------------------------
-- Plot Cultivars Table

CREATE TABLE IF NOT EXISTS gemini.plot_cultivars (
    plot_id UUID REFERENCES gemini.plots(id) ON DELETE CASCADE,
    cultivar_id UUID REFERENCES gemini.cultivars(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (plot_id, cultivar_id)
);

-------------------------------------------------------------------------------
-- Trait Sensors Table

CREATE TABLE IF NOT EXISTS gemini.trait_sensors (
    trait_id UUID REFERENCES gemini.traits(id) ON DELETE CASCADE,
    sensor_id UUID REFERENCES gemini.sensors(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (trait_id, sensor_id)
);

-------------------------------------------------------------------------------
-- Sensor Platforms Sensors Table

CREATE TABLE IF NOT EXISTS gemini.sensor_platform_sensors (
    sensor_platform_id UUID REFERENCES gemini.sensor_platforms(id) ON DELETE CASCADE,
    sensor_id UUID REFERENCES gemini.sensors(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (sensor_platform_id, sensor_id)
);

-------------------------------------------------------------------------------
-- Sensor Datasets Table

CREATE TABLE IF NOT EXISTS gemini.sensor_datasets (
    sensor_id UUID REFERENCES gemini.sensors(id) ON DELETE CASCADE,
    dataset_id UUID REFERENCES gemini.datasets(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (sensor_id, dataset_id)
);

-------------------------------------------------------------------------------
-- Trait Datasets Table

CREATE TABLE IF NOT EXISTS gemini.trait_datasets (
    trait_id UUID REFERENCES gemini.traits(id) ON DELETE CASCADE,
    dataset_id UUID REFERENCES gemini.datasets(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (trait_id, dataset_id)
);

-------------------------------------------------------------------------------
-- Model Datasets Table

CREATE TABLE IF NOT EXISTS gemini.model_datasets (
    model_id UUID REFERENCES gemini.models(id) ON DELETE CASCADE,
    dataset_id UUID REFERENCES gemini.datasets(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (model_id, dataset_id)
);

-------------------------------------------------------------------------------
-- Script Datasets Table

CREATE TABLE IF NOT EXISTS gemini.script_datasets (
    script_id UUID REFERENCES gemini.scripts(id) ON DELETE CASCADE,
    dataset_id UUID REFERENCES gemini.datasets(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (script_id, dataset_id)
);

-------------------------------------------------------------------------------
-- Procedure Datasets Table

CREATE TABLE IF NOT EXISTS gemini.procedure_datasets (
    procedure_id UUID REFERENCES gemini.procedures(id) ON DELETE CASCADE,
    dataset_id UUID REFERENCES gemini.datasets(id) ON DELETE CASCADE,
    info JSONB DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (procedure_id, dataset_id)
);

