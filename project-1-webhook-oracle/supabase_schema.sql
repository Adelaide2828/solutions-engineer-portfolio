-- ==============================================================================
-- PROJECT 1: COLD CHAIN SENSOR ORACLE - POSTGRESQL (SUPABASE) DDL SCHEMA
-- ==============================================================================

-- 1. Enable UUID Extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Clean Validated Sensor Readings Table
CREATE TABLE IF NOT EXISTS sensor_readings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id UUID NOT NULL UNIQUE,
    facility_id VARCHAR(10) NOT NULL,
    reading_timestamp TIMESTAMPTZ NOT NULL,
    temperature_c NUMERIC(5, 2) NOT NULL,
    humidity_pct NUMERIC(5, 2) NOT NULL,
    sensor_status VARCHAR(20) NOT NULL,
    ingested_at TIMESTAMPTZ DEFAULT NOW(),

    -- Strict Data Integrity Check Constraints
    CONSTRAINT chk_temperature_bounds CHECK (temperature_c >= -25.0 AND temperature_c <= 15.0),
    CONSTRAINT chk_humidity_bounds CHECK (humidity_pct >= 0.0 AND humidity_pct <= 100.0),
    CONSTRAINT chk_facility_code CHECK (facility_id ~ '^FAC-[0-9]{3}$'),
    CONSTRAINT chk_status_enum CHECK (sensor_status IN ('ONLINE', 'CALIBRATING', 'DEGRADED'))
);

-- Indexes for Fast Analytics & Time-Series Aggregations
CREATE INDEX IF NOT EXISTS idx_sensor_facility_time ON sensor_readings (facility_id, reading_timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_sensor_status ON sensor_readings (sensor_status);

-- 3. Anomaly Quarantine Table for Rejected Payloads
CREATE TABLE IF NOT EXISTS anomaly_quarantine (
    quarantine_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id VARCHAR(100),
    facility_id VARCHAR(50),
    raw_payload JSONB NOT NULL,
    rejection_reason TEXT NOT NULL,
    flagged_temperature NUMERIC(5, 2),
    resolved BOOLEAN DEFAULT FALSE,
    resolution_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for ops review queue
CREATE INDEX IF NOT EXISTS idx_quarantine_unresolved ON anomaly_quarantine (created_at DESC) WHERE resolved = FALSE;

-- 4. Analytical Summary View for Solutions Engineering KPI Dashboards
CREATE OR REPLACE VIEW v_facility_health_summary AS
SELECT 
    facility_id,
    COUNT(*) AS total_clean_readings,
    ROUND(AVG(temperature_c), 2) AS avg_temperature_c,
    MIN(temperature_c) AS min_temperature_c,
    MAX(temperature_c) AS max_temperature_c,
    ROUND(AVG(humidity_pct), 2) AS avg_humidity_pct,
    MAX(reading_timestamp) AS last_reported_at
FROM sensor_readings
GROUP BY facility_id;
