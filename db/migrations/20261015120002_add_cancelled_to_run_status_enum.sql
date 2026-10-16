-- Add 'cancelled' status to run_status enum
ALTER TYPE agents.run_status ADD VALUE 'cancelled';

-- migrate:down
-- Note: Cannot remove enum values in PostgreSQL without recreating the type
-- If needed to downgrade, manually:
-- 1. ALTER TABLE agents.runs ALTER COLUMN status TYPE TEXT;
-- 2. DROP TYPE agents.run_status;
-- 3. CREATE TYPE agents.run_status AS ENUM ('queued', 'running', 'completed', 'failed');
-- 4. ALTER TABLE agents.runs ALTER COLUMN status TYPE agents.run_status;
