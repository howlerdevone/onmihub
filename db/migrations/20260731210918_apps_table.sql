-- migrate:up
CREATE SCHEMA IF NOT EXISTS catalog;

-- 1. Supported MCP Applications Catalog
CREATE TABLE catalog.apps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon_url TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Business Areas / Departments Catalog
CREATE TABLE catalog.areas (
    id VARCHAR(50) PRIMARY KEY,                   -- Strict human-readable identifier (e.g., 'finance', 'management')
    name VARCHAR(100) NOT NULL,                  -- Display name for the onboarding UI (e.g., 'Finance & Accounting')
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 3. Intermediary Matrix for Onboarding Recommendations (Many-to-Many)
CREATE TABLE catalog.app_areas (
    app_id UUID NOT NULL REFERENCES catalog.apps(id) ON DELETE CASCADE,
    area_id VARCHAR(50) NOT NULL REFERENCES catalog.areas(id) ON DELETE CASCADE,
    PRIMARY KEY (app_id, area_id)
);

-- 4. Operational performance indexing
CREATE INDEX idx_catalog_app_areas_lookup ON catalog.app_areas (area_id);


-- --- SEED DATA: Populating default platform taxonomy ---

-- Insert Applications (MCP Ecosystem)
INSERT INTO catalog.apps (name, description) VALUES
    ('Google Drive', 'Index docs, spreadsheets and PDFs from your cloud storage'),
    ('Outlook Mail', 'Connect your business email to read and analyze messages'),
    ('Notion', 'Sync your corporate wikis, databases and documentation pages'),
    ('QuickBooks', 'Analyze invoices, expenses and accounting balance sheets');

-- Insert Areas
INSERT INTO catalog.areas (id, name) VALUES
    ('finance', 'Finance & Accounting'),
    ('management', 'Operations & Management'),
    ('legal', 'Legal & Compliance');

-- Map Matrix (Recommendations Engine)
-- If user selects 'finance' -> recommend Google Drive and QuickBooks
INSERT INTO catalog.app_areas (app_id, area_id)
SELECT id, 'finance' FROM catalog.apps WHERE name = 'Google Drive'
UNION ALL
SELECT id, 'finance' FROM catalog.apps WHERE name = 'QuickBooks';

-- If user selects 'management' -> recommend Google Drive, Outlook and Notion
INSERT INTO catalog.app_areas (app_id, area_id)
SELECT id, 'management' FROM catalog.apps WHERE name = 'Google Drive'
UNION ALL
SELECT id, 'management' FROM catalog.apps WHERE name = 'Outlook Mail'
UNION ALL
SELECT id, 'management' FROM catalog.apps WHERE name = 'Notion';

-- If user selects 'legal' -> recommend Google Drive and Notion
INSERT INTO catalog.app_areas (app_id, area_id)
SELECT id, 'legal' FROM catalog.apps WHERE name = 'Google Drive'
UNION ALL
SELECT id, 'legal' FROM catalog.apps WHERE name = 'Notion';

-- migrate:down

DROP TABLE IF EXISTS catalog.app_areas;
DROP TABLE IF EXISTS catalog.areas;
DROP TABLE IF EXISTS catalog.apps;
DROP SCHEMA IF EXISTS catalog;
