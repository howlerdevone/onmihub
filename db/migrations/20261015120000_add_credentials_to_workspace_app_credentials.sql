-- Add credentials column to workspace_app_credentials for MVP (plaintext until KSM is implemented)
ALTER TABLE organizations.workspace_app_credentials
ADD COLUMN credentials JSONB NOT NULL DEFAULT '{}';

-- migrate:down
ALTER TABLE organizations.workspace_app_credentials
DROP COLUMN IF EXISTS credentials;
