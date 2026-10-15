-- migrate:up

-- Add onboarding_completed_at column to identity.users
ALTER TABLE identity.users
  ADD COLUMN IF NOT EXISTS onboarding_completed_at TIMESTAMP WITH TIME ZONE DEFAULT NULL;

-- Create index for efficient filtering of users who completed onboarding
CREATE INDEX IF NOT EXISTS idx_users_onboarding_completed_at
  ON identity.users (onboarding_completed_at);

-- migrate:down

DROP INDEX IF EXISTS identity.idx_users_onboarding_completed_at;
ALTER TABLE identity.users
  DROP COLUMN IF EXISTS onboarding_completed_at;
