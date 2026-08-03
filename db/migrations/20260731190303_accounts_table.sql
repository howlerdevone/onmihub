-- migrate:up

CREATE SCHEMA IF NOT EXISTS auth;

CREATE TYPE auth.provider_enum AS ENUM ('local', 'google', 'github', 'apple', 'microsoft');

CREATE TABLE auth.accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    
    provider auth.provider_enum NOT NULL,
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

CREATE INDEX idx_auth_accounts_lookup ON auth.accounts (provider, provider_user_id);
CREATE INDEX idx_auth_accounts_user_id ON auth.accounts (user_id);

-- migrate:down

DROP TABLE IF EXISTS auth.accounts;
DROP TYPE IF EXISTS auth.provider_enum;
DROP SCHEMA IF EXISTS auth;
