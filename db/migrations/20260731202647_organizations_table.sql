-- migrate:up
CREATE SCHEMA IF NOT EXISTS organizations;

-- Strict enum for workspace permission management
CREATE TYPE organizations.workspace_role_enum AS ENUM ('owner', 'admin', 'member');

-- 1. Create the master registry for all system capabilities (Permissions)
CREATE TABLE organizations.permissions (
    id VARCHAR(50) PRIMARY KEY,                   -- Human-readable strict ID (e.g., 'files:create', 'mcp:manage')
    description TEXT NOT NULL,                    -- Explanation of what this capability grants
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create the mapping table to assign capabilities to roles
CREATE TABLE organizations.role_permissions (
    role organizations.workspace_role_enum NOT NULL, -- Our previously created ENUM ('owner', 'admin', 'member')
    permission_id VARCHAR(50) NOT NULL REFERENCES organizations.permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role, permission_id)
);

-- Master Workspace Table (The corporate or individual container)
CREATE TABLE organizations.workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(120) NOT NULL UNIQUE,            -- URL-safe identifier (e.g., 'omnihub-finances-team')
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Memberships Table (The secure link between Users and Workspaces)
CREATE TABLE organizations.memberships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES organizations.workspaces(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    role organizations.workspace_role_enum NOT NULL DEFAULT 'member',
    
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- A user can only hold exactly one membership record per workspace
    CONSTRAINT unique_user_workspace_membership UNIQUE (workspace_id, user_id)
);



-- 3. High-performance index to check permission grants instantly during API calls
CREATE INDEX idx_organizations_memberships_user ON organizations.memberships (user_id);
CREATE INDEX idx_organizations_memberships_workspace ON organizations.memberships (workspace_id);

-- --- SEED DATA: Populating default platform permissions ---

INSERT INTO organizations.permissions (id, description) VALUES
    ('workspace:update', 'Allows updating workspace general settings and profile'),
    ('workspace:delete', 'Allows complete destruction of the workspace and its data'),
    ('members:invite',   'Allows inviting new users to join the workspace'),
    ('members:manage',   'Allows changing roles or revoking access from current members'),
    ('files:create',     'Allows creating virtual folders and uploading new files'),
    ('files:view',       'Allows viewing, reading, and querying workspace files through the AI or web'),
    ('files:delete',     'Allows permanent deletion of stored files and directories'),
    ('mcp:connect',      'Allows linking third-party apps like Google Drive or Outlook via MCP'),
    ('mcp:disconnect',   'Allows revoking access from connected external integrations'),
    ('chat:manage',      'Allows configuring or binding communication channels like WhatsApp or Telegram'),
    ('billing:manage',   'Allows viewing invoices, changing subscription plans, or managing payments')
ON CONFLICT (id) DO NOTHING;

-- --- SEED DATA: Mapping capabilities to roles (The Permission Matrix) ---

-- OWNER: Has access to absolutely everything
INSERT INTO organizations.role_permissions (role, permission_id)
SELECT 'owner', id FROM organizations.permissions
ON CONFLICT (role, permission_id) DO NOTHING;

-- ADMIN: Can manage data and members, but cannot touch billing or destroy the workspace
INSERT INTO organizations.role_permissions (role, permission_id) VALUES
    ('admin', 'workspace:update'),
    ('admin', 'members:invite'),
    ('admin', 'members:manage'),
    ('admin', 'files:create'),
    ('admin', 'files:view'),
    ('admin', 'files:delete'),
    ('admin', 'mcp:connect'),
    ('admin', 'mcp:disconnect'),
    ('admin', 'chat:manage')
ON CONFLICT (role, permission_id) DO NOTHING;

-- MEMBER: Safe worker. Can only view/upload files and chat. Cannot touch infrastructure.
INSERT INTO organizations.role_permissions (role, permission_id) VALUES
    ('member', 'files:create'),
    ('member', 'files:view')
ON CONFLICT (role, permission_id) DO NOTHING;

-- migrate:down
DROP TABLE IF EXISTS organizations.role_permissions;
DROP TABLE IF EXISTS organizations.permissions; 
DROP TABLE IF EXISTS organizations.memberships;
DROP TABLE IF EXISTS organizations.workspaces;
DROP TYPE IF EXISTS organizations.workspace_role_enum;
DROP SCHEMA IF EXISTS organizations CASCADE;