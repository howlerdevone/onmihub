-- migrate:up

-- Ensure schema exists
CREATE SCHEMA IF NOT EXISTS identity;

-- Drop constraints that depend on user_id
ALTER TABLE identity.accounts
  DROP CONSTRAINT IF EXISTS unique_user_provider;

DROP INDEX IF EXISTS idx_identity_accounts_user_id;

-- Drop the user_id column
ALTER TABLE identity.accounts
  DROP COLUMN IF EXISTS user_id;

-- migrate:down

-- No rollback available - this is a destructive migration
