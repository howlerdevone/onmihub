-- Add events table for auditing agent execution
CREATE TABLE agents.events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  run_id UUID NOT NULL REFERENCES agents.runs(id) ON DELETE CASCADE,
  event_type TEXT NOT NULL,
  data JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX idx_events_run_id ON agents.events(run_id);
CREATE INDEX idx_events_created_at ON agents.events(created_at);
