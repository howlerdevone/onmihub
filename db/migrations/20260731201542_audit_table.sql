-- migrate:up
CREATE SCHEMA IF NOT EXISTS audit;

-- 1. Strict classification for system anomalies
CREATE TYPE audit.log_level_enum AS ENUM ('info', 'warning', 'error', 'critical');

-- 2. Capture platform crashes and background failures
CREATE TABLE audit.system_errors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    level audit.log_level_enum NOT NULL DEFAULT 'error',

    -- Telemetry origin data
    endpoint VARCHAR(255),                        -- Web path or background task name (e.g., 'tasks.sync_mcp_drive')
    method VARCHAR(10),                           -- HTTP Verb (GET, POST) or NULL if triggered by Celery

    -- Error payload
    error_message TEXT NOT NULL,                  -- Short description of the exception
    traceback TEXT,                               -- Full Python traceback trace containing exact file lines

    -- Contextual relationship
    user_id UUID REFERENCES identity.users(id) ON DELETE SET NULL, -- Retain system bugs even if the user profile is deleted

    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 3. Maintain historical record of dangerous mutations
CREATE TABLE audit.activity_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id) ON DELETE CASCADE, -- Remove activity logs if the account is erased

    -- Action fingerprint
    action VARCHAR(100) NOT NULL,                 -- Action identifier (e.g., 'file.purge', 'mcp.disconnect')

    -- Target descriptor (Basic polymorphic routing)
    entity_type VARCHAR(50) NOT NULL,            -- Targeted entity table name (e.g., 'files', 'accounts')
    entity_id UUID NOT NULL,                      -- Targeted entity primary key

    -- Network metadata
    ip_address VARCHAR(45),                       -- Client IP address (Supports IPv4 and IPv6)
    user_agent TEXT,                              -- Browser or client hardware signature

    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 4. High-performance operational indexing
CREATE INDEX idx_audit_system_errors_level ON audit.system_errors (level);
CREATE INDEX idx_audit_system_errors_user ON audit.system_errors (user_id);
CREATE INDEX idx_audit_activity_logs_user_action ON audit.activity_logs (user_id, action);
CREATE INDEX idx_audit_activity_logs_target ON audit.activity_logs (entity_type, entity_id);

-- migrate:down
DROP TABLE IF EXISTS audit.activity_logs;
DROP TABLE IF EXISTS audit.system_errors;
DROP TYPE IF EXISTS audit.log_level_enum;
DROP SCHEMA IF EXISTS audit;
