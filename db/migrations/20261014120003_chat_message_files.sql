-- Add message_files table for tracking persistent files attached to messages
CREATE TABLE chat.message_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  message_id UUID NOT NULL REFERENCES chat.messages(id) ON DELETE CASCADE,
  conversation_id UUID NOT NULL REFERENCES chat.conversations(id) ON DELETE CASCADE,
  workspace_id UUID NOT NULL REFERENCES organizations.workspaces(id) ON DELETE CASCADE,
  filename TEXT NOT NULL,
  gcs_path TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX idx_message_files_message_id ON chat.message_files(message_id);
CREATE INDEX idx_message_files_conversation_id ON chat.message_files(conversation_id);
CREATE INDEX idx_message_files_workspace_id ON chat.message_files(workspace_id);
