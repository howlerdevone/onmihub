-- migrate:up

CREATE TABLE organizations.workspace_app_credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES organizations.workspaces(id) ON DELETE CASCADE,
    app_id UUID NOT NULL REFERENCES catalog.apps(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES identity.users(id) ON DELETE CASCADE,
    ksm_key TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_workspace_app_user_credential UNIQUE (workspace_id, app_id, user_id)
);

CREATE INDEX idx_organizations_workspace_app_credentials_workspace ON organizations.workspace_app_credentials (workspace_id);
CREATE INDEX idx_organizations_workspace_app_credentials_user ON organizations.workspace_app_credentials (user_id);

-- migrate:down

DROP TABLE IF EXISTS organizations.workspace_app_credentials;
