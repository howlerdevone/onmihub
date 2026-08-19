-- migrate:up

CREATE TABLE organizations.workspace_apps (
    workspace_id UUID NOT NULL REFERENCES organizations.workspaces(id) ON DELETE CASCADE,
    app_id UUID NOT NULL REFERENCES catalog.apps(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (workspace_id, app_id)
);

CREATE INDEX idx_organizations_workspace_apps_app ON organizations.workspace_apps (app_id);

-- migrate:down

DROP TABLE IF EXISTS organizations.workspace_apps;
