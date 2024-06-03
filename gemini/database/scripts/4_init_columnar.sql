-- ------------------------------------------------------------------------------
-- -- Columnar Tables (using Hydra)
-- ------------------------------------------------------------------------------

------------------------------------------------------------------------------
-- Dataset Records Table
------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gemini.dataset_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    collection_date DATE NOT NULL DEFAULT CURRENT_DATE,
    dataset_id UUID,
    dataset_name TEXT,
    dataset_data JSONB NOT NULL DEFAULT '{}',
    record_info JSONB NOT NULL DEFAULT '{}'
) USING columnar;


ALTER TABLE gemini.dataset_records ADD CONSTRAINT dataset_records_unique UNIQUE NULLS DISTINCT (timestamp, collection_date, dataset_id, dataset_name, record_info);

------------------------------------------------------------------------------
-- Sensor Records Table
------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gemini.sensor_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    collection_date DATE NOT NULL DEFAULT CURRENT_DATE,
    dataset_id UUID,
    dataset_name TEXT,
    sensor_id UUID,
    sensor_name TEXT,
    sensor_data JSONB NOT NULL DEFAULT '{}',
    record_info JSONB NOT NULL DEFAULT '{}'
);

ALTER TABLE gemini.sensor_records ADD CONSTRAINT sensor_records_unique UNIQUE NULLS DISTINCT (timestamp, collection_date, dataset_id, dataset_name, sensor_id, sensor_name, record_info);


------------------------------------------------------------------------------
-- Trait Records Table
------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gemini.trait_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    collection_date DATE NOT NULL DEFAULT CURRENT_DATE,
    dataset_id UUID,
    dataset_name TEXT,
    trait_id UUID,
    trait_name TEXT,
    trait_value REAL NOT NULL DEFAULT 0.0,
    record_info JSONB NOT NULL DEFAULT '{}'
) USING columnar;

ALTER TABLE gemini.trait_records ADD CONSTRAINT trait_records_unique UNIQUE NULLS DISTINCT (timestamp, collection_date, dataset_id, dataset_name, trait_id, trait_name, record_info);


------------------------------------------------------------------------------
-- Procedure Records Table
------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gemini.procedure_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    collection_date DATE NOT NULL DEFAULT CURRENT_DATE,
    dataset_id UUID,
    dataset_name TEXT,
    procedure_id UUID,
    procedure_name TEXT,
    procedure_data JSONB NOT NULL DEFAULT '{}',
    record_info JSONB NOT NULL DEFAULT '{}'
) USING columnar;

ALTER TABLE gemini.procedure_records ADD CONSTRAINT procedure_records_unique UNIQUE NULLS DISTINCT (timestamp, collection_date, dataset_id, dataset_name, procedure_id, procedure_name, record_info);


------------------------------------------------------------------------------
-- Script Records Table
------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gemini.script_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    collection_date DATE NOT NULL DEFAULT CURRENT_DATE,
    dataset_id UUID,
    dataset_name TEXT,
    script_id UUID,
    script_name TEXT,
    script_data JSONB NOT NULL DEFAULT '{}',
    record_info JSONB NOT NULL DEFAULT '{}'
) USING columnar;

ALTER TABLE gemini.script_records ADD CONSTRAINT script_records_unique UNIQUE NULLS DISTINCT (timestamp, collection_date, dataset_id, dataset_name, script_id, script_name, record_info);


------------------------------------------------------------------------------
-- Model Records Table
------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gemini.model_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    collection_date DATE NOT NULL DEFAULT CURRENT_DATE,
    dataset_id UUID,
    dataset_name TEXT,
    model_id UUID,
    model_name TEXT,
    model_data JSONB NOT NULL DEFAULT '{}',
    record_info JSONB NOT NULL DEFAULT '{}'
) USING columnar;

ALTER TABLE gemini.model_records ADD CONSTRAINT model_records_unique UNIQUE NULLS DISTINCT (timestamp, collection_date, dataset_id, dataset_name, model_id, model_name, record_info);

