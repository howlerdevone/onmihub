-- migrate:up

ALTER TABLE organizations.workspaces
  ADD COLUMN IF NOT EXISTS created_by UUID;

ALTER TABLE organizations.workspaces
  ADD CONSTRAINT fk_organizations_workspaces_created_by
  FOREIGN KEY (created_by)
  REFERENCES auth.users(id)
  ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_organizations_workspaces_created_by
  ON organizations.workspaces (created_by);

-- migrate:down

DROP INDEX IF EXISTS idx_organizations_workspaces_created_by;
ALTER TABLE organizations.workspaces DROP CONSTRAINT IF EXISTS fk_organizations_workspaces_created_by;
ALTER TABLE organizations.workspaces DROP COLUMN IF EXISTS created_by;
