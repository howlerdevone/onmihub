-- migrate:up

CREATE SCHEMA IF NOT EXISTS identity;

CREATE TABLE identity.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT,
    display_name TEXT,
    avatar_url TEXT,
    preferred_language TEXT,
    timezone TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_identity_users_email ON identity.users (email);

-- migrate:down

DROP TABLE IF EXISTS identity.users;
DROP SCHEMA IF EXISTS identity;
