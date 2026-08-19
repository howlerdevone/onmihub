-- migrate:up

ALTER TABLE catalog.apps
  ADD COLUMN url TEXT,
  ADD COLUMN mcp_auth_config_template JSONB;

-- migrate:down

ALTER TABLE catalog.apps
  DROP COLUMN IF EXISTS mcp_auth_config_template,
  DROP COLUMN IF EXISTS url;
