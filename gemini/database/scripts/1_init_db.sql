-------------------------------------------------------------------------------
-- Initialize Database, Schema and Plugins
-------------------------------------------------------------------------------

-- Create a schema for the GEMINI Database
CREATE SCHEMA IF NOT EXISTS gemini;

-- Initialize Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- Used for generating UUIDs
CREATE EXTENSION IF NOT EXISTS "pgcrypto"; -- Used for generating passwords
CREATE EXTENSION IF NOT EXISTS columnar; -- Used for columnar storage

ALTER DATABASE gemini_db SET default_table_access_method = 'heap';
