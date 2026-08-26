-- migrate:up
ALTER TABLE assets.files
ADD COLUMN workspace_id UUID NOT NULL;

ALTER TABLE assets.files
ADD CONSTRAINT fk_files_workspace_id FOREIGN KEY (workspace_id)
  REFERENCES organizations.workspaces(id) ON DELETE CASCADE;

CREATE INDEX idx_assets_files_workspace ON assets.files (workspace_id);

-- Update the unique constraint to include workspace_id
ALTER TABLE assets.files
DROP CONSTRAINT unique_filename_per_folder;

ALTER TABLE assets.files
ADD CONSTRAINT unique_filename_per_folder_workspace UNIQUE (workspace_id, owner_id, parent_id, name, is_folder);

-- migrate:down
ALTER TABLE assets.files
DROP CONSTRAINT unique_filename_per_folder_workspace;

ALTER TABLE assets.files
ADD CONSTRAINT unique_filename_per_folder UNIQUE (owner_id, parent_id, name, is_folder);

DROP INDEX IF EXISTS idx_assets_files_workspace;

ALTER TABLE assets.files
DROP CONSTRAINT fk_files_workspace_id;

ALTER TABLE assets.files
DROP COLUMN workspace_id;
