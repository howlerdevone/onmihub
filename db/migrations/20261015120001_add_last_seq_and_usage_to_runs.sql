-- Add last_seq and usage to agents.runs table
ALTER TABLE agents.runs
ADD COLUMN last_seq INT,
ADD COLUMN usage JSONB;

-- migrate:down
ALTER TABLE agents.runs
DROP COLUMN IF EXISTS last_seq,
DROP COLUMN IF EXISTS usage;
