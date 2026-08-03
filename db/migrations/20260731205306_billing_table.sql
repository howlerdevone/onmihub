-- migrate:up
CREATE SCHEMA IF NOT EXISTS billing;

-- Enum of supported plan ids
CREATE TYPE billing.plan_enum AS ENUM ('free', 'pro');

-- 1. Product Catalog Master Table
CREATE TABLE billing.plans (
    id billing.plan_enum PRIMARY KEY,                   -- Strict plan ID (enum: 'free', 'pro')
    name VARCHAR(100) NOT NULL,                   -- Visible name (e.g., 'Omnihub Pro')
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Granular Rules Matrix for System Constraints (Key-Value Strategy)
CREATE TABLE billing.plan_limits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id billing.plan_enum NOT NULL REFERENCES billing.plans(id) ON DELETE CASCADE,
    
    limit_key VARCHAR(100) NOT NULL,              -- Target constraint identifier (e.g., 'max_storage_bytes', 'max_mcp_connections')
    limit_value BIGINT NOT NULL,                  -- Quantitative limit boundary (BIGINT avoids integer overflows for bytes or numbers)
    
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Prevent duplicate rule definitions for the exact same plan
    CONSTRAINT unique_plan_limit_key UNIQUE (plan_id, limit_key)
);

-- 3. Active Subscription Ledger for Tenant Workspaces
CREATE TABLE billing.subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL UNIQUE REFERENCES organizations.workspaces(id) ON DELETE CASCADE, -- Bound strictly to the workspace
    plan_id billing.plan_enum NOT NULL REFERENCES billing.plans(id),
    
    status VARCHAR(50) NOT NULL DEFAULT 'active', -- Lifecycle states (e.g., 'active', 'past_due', 'canceled', 'trialing')
    current_period_end TIMESTAMP WITH TIME ZONE,  -- Synchronization timestamp for downstream payment gateways (e.g., Stripe)
    
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 4. High-efficiency database indexing
CREATE INDEX idx_billing_plan_limits_lookup ON billing.plan_limits (plan_id, limit_key);
CREATE INDEX idx_billing_subscriptions_workspace ON billing.subscriptions (workspace_id);


-- --- SEED DATA: Populating default business models and limit rules ---

-- Insert Plans
INSERT INTO billing.plans (id, name, description) VALUES
    ('free', 'Omnihub Free', 'Basic evaluation plan for single individuals'),
    ('pro', 'Omnihub Pro', 'Advanced orchestration tools for growing teams')
ON CONFLICT (id) DO NOTHING;

-- Insert Rules for Free Plan
INSERT INTO billing.plan_limits (plan_id, limit_key, limit_value) VALUES
    ('free', 'max_storage_bytes', 1073741824),    -- 1 GB in bytes
    ('free', 'max_mcp_connections', 2),          -- Max 2 external apps linked (e.g., just Google Drive)
    ('free', 'max_workspace_members', 1),        -- Solo workspace
    ('free', 'max_monthly_messages', 200)       -- Limit AI chat usage
ON CONFLICT (plan_id, limit_key) DO NOTHING;

-- Insert Rules for Pro Plan
INSERT INTO billing.plan_limits (plan_id, limit_key, limit_value) VALUES
    ('pro', 'max_storage_bytes', 53687091200),    -- 50 GB in bytes
    ('pro', 'max_mcp_connections', 10),          -- Up to 10 integrations
    ('pro', 'max_workspace_members', 5),         -- Small collaborative team
    ('pro', 'max_monthly_messages', 5000)       -- High volume chat usage
ON CONFLICT (plan_id, limit_key) DO NOTHING;

-- migrate:down
DROP TABLE IF EXISTS billing.subscriptions;
DROP TABLE IF EXISTS billing.plan_limits;
DROP TABLE IF EXISTS billing.plans;
DROP TYPE IF EXISTS billing.plan_enum;
DROP SCHEMA IF EXISTS billing;