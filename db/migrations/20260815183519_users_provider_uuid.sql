-- migrate:up

ALTER TABLE auth.users
  ADD COLUMN IF NOT EXISTS provider_id UUID;

CREATE INDEX IF NOT EXISTS idx_auth_users_provider_id
  ON auth.users (provider_id);

-- migrate:down

DROP INDEX IF EXISTS idx_auth_users_provider_id;
ALTER TABLE auth.users
  DROP COLUMN IF EXISTS provider_id;
