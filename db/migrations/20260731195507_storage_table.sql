-- migrate:up
CREATE SCHEMA IF NOT EXISTS storage;

CREATE TYPE storage.file_status_enum AS ENUM ('pending', 'processing', 'ready', 'failed');

CREATE TABLE storage.files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    owner_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    
    parent_id UUID REFERENCES storage.files(id) ON DELETE CASCADE,
    
    is_folder BOOLEAN NOT NULL DEFAULT FALSE,
    name VARCHAR(255) NOT NULL,
    
    storage_path TEXT,
    
    mime_type VARCHAR(100),             
    size_bytes BIGINT DEFAULT 0,
    status storage.file_status_enum NOT NULL DEFAULT 'pending',
    
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_filename_per_folder UNIQUE (owner_id, parent_id, name, is_folder)
);

CREATE INDEX idx_storage_files_owner ON storage.files (owner_id);
CREATE INDEX idx_storage_files_parent ON storage.files (parent_id);
CREATE INDEX idx_storage_files_status ON storage.files (status);

-- migrate:down
DROP TABLE IF EXISTS storage.files;
DROP TYPE IF EXISTS storage.file_status_enum;
DROP SCHEMA IF EXISTS storage;