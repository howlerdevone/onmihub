-- migrate:up

CREATE SCHEMA IF NOT EXISTS identity;

CREATE TYPE identity.provider_enum AS ENUM ('local', 'google', 'github', 'apple', 'microsoft');

CREATE TABLE identity.accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id) ON DELETE CASCADE,

    provider identity.provider_enum NOT NULL,
    provider_user_id VARCHAR(255) NOT NULL,
    access_token TEXT,
    refresh_token TEXT,
    expires_at TIMESTAMP WITH TIME ZONE,
    scope TEXT,

    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_user_provider UNIQUE (user_id, provider),
    CONSTRAINT unique_provider_identity UNIQUE (provider, provider_user_id)
);

CREATE INDEX idx_identity_accounts_lookup ON identity.accounts (provider, provider_user_id);
CREATE INDEX idx_identity_accounts_user_id ON identity.accounts (user_id);

-- migrate:down

DROP TABLE IF EXISTS identity.accounts;
DROP TYPE IF EXISTS identity.provider_enum;
DROP SCHEMA IF EXISTS identity;
