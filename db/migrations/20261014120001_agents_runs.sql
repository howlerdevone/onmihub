-- Create agents schema and runs table for ephemeral agent execution tracking
CREATE SCHEMA IF NOT EXISTS agents;

-- Run status enum
CREATE TYPE agents.run_status AS ENUM ('queued', 'running', 'completed', 'failed');

-- Agent runs table (internal, invisible to frontend)
CREATE TABLE agents.runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL,
  user_id UUID NOT NULL,
  conversation_id UUID NOT NULL,
  message_id UUID NOT NULL,
  status agents.run_status NOT NULL DEFAULT 'queued',
  run_token TEXT NOT NULL UNIQUE,
  manifest JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  completed_at TIMESTAMP WITH TIME ZONE,

  CONSTRAINT fk_runs_workspace FOREIGN KEY (workspace_id) REFERENCES organizations.workspaces(id) ON DELETE CASCADE,
  CONSTRAINT fk_runs_user FOREIGN KEY (user_id) REFERENCES identity.users(id) ON DELETE CASCADE,
  CONSTRAINT fk_runs_conversation FOREIGN KEY (conversation_id) REFERENCES chat.conversations(id) ON DELETE CASCADE,
  CONSTRAINT fk_runs_message FOREIGN KEY (message_id) REFERENCES chat.messages(id) ON DELETE CASCADE
);

CREATE INDEX idx_runs_workspace_id ON agents.runs(workspace_id);
CREATE INDEX idx_runs_user_id ON agents.runs(user_id);
CREATE INDEX idx_runs_conversation_id ON agents.runs(conversation_id);
CREATE INDEX idx_runs_status ON agents.runs(status);
CREATE INDEX idx_runs_created_at ON agents.runs(created_at);
