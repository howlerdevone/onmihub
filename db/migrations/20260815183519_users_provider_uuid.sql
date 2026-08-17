-- migrate:up

ALTER TABLE identity.users
  ADD COLUMN IF NOT EXISTS provider_id UUID;

CREATE INDEX IF NOT EXISTS idx_identity_users_provider_id
  ON identity.users (provider_id);

-- migrate:down

DROP INDEX IF EXISTS idx_identity_users_provider_id;
ALTER TABLE identity.users
  DROP COLUMN IF EXISTS provider_id;
