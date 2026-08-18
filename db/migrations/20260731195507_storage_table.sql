-- migrate:up
CREATE SCHEMA IF NOT EXISTS assets;

CREATE TYPE assets.file_status_enum AS ENUM ('pending', 'processing', 'ready', 'failed');

CREATE TABLE assets.files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    owner_id UUID NOT NULL REFERENCES identity.users(id) ON DELETE CASCADE,

    parent_id UUID REFERENCES assets.files(id) ON DELETE CASCADE,

    is_folder BOOLEAN NOT NULL DEFAULT FALSE,
    name VARCHAR(255) NOT NULL,

    storage_path TEXT,

    mime_type VARCHAR(100),
    size_bytes BIGINT DEFAULT 0,
    status assets.file_status_enum NOT NULL DEFAULT 'pending',

    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_filename_per_folder UNIQUE (owner_id, parent_id, name, is_folder)
);

CREATE INDEX idx_assets_files_owner ON assets.files (owner_id);
CREATE INDEX idx_assets_files_parent ON assets.files (parent_id);
CREATE INDEX idx_assets_files_status ON assets.files (status);

-- migrate:down
DROP TABLE IF EXISTS assets.files;
DROP TYPE IF EXISTS assets.file_status_enum;
DROP SCHEMA IF EXISTS assets;
