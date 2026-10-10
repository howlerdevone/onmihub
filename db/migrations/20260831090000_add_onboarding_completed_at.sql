-- Add onboarding_completed_at column to identity.users
ALTER TABLE identity.users
ADD COLUMN onboarding_completed_at TIMESTAMP WITH TIME ZONE DEFAULT NULL;

-- Create index for efficient filtering of users who completed onboarding
CREATE INDEX idx_users_onboarding_completed_at
ON identity.users(onboarding_completed_at);
