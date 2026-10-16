-- Create chat schema and related types/tables for conversations and messages
CREATE SCHEMA IF NOT EXISTS chat;

-- Message sender enum
CREATE TYPE chat.message_sender AS ENUM ('user', 'bot', 'system');

-- Message source enum (where the message came from)
CREATE TYPE chat.message_source AS ENUM ('web', 'whatsapp', 'telegram');

-- Conversations table
CREATE TABLE chat.conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL,
  user_id UUID NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),

  CONSTRAINT fk_conversations_workspace FOREIGN KEY (workspace_id) REFERENCES organizations.workspaces(id) ON DELETE CASCADE,
  CONSTRAINT fk_conversations_user FOREIGN KEY (user_id) REFERENCES identity.users(id) ON DELETE CASCADE
);

CREATE INDEX idx_conversations_workspace_id ON chat.conversations(workspace_id);
CREATE INDEX idx_conversations_user_id ON chat.conversations(user_id);

-- Messages table
CREATE TABLE chat.messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL,
  sender chat.message_sender NOT NULL,
  content TEXT NOT NULL,
  source chat.message_source NOT NULL DEFAULT 'web',
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),

  CONSTRAINT fk_messages_conversation FOREIGN KEY (conversation_id) REFERENCES chat.conversations(id) ON DELETE CASCADE
);

CREATE INDEX idx_messages_conversation_id ON chat.messages(conversation_id);

-- Message files table (persistent files in GCS)
CREATE TABLE chat.message_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  message_id UUID NOT NULL,
  conversation_id UUID NOT NULL,
  workspace_id UUID NOT NULL,
  filename TEXT NOT NULL,
  gcs_path TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),

  CONSTRAINT fk_message_files_message FOREIGN KEY (message_id) REFERENCES chat.messages(id) ON DELETE CASCADE,
  CONSTRAINT fk_message_files_conversation FOREIGN KEY (conversation_id) REFERENCES chat.conversations(id) ON DELETE CASCADE,
  CONSTRAINT fk_message_files_workspace FOREIGN KEY (workspace_id) REFERENCES organizations.workspaces(id) ON DELETE CASCADE
);

CREATE INDEX idx_message_files_message_id ON chat.message_files(message_id);
CREATE INDEX idx_message_files_conversation_id ON chat.message_files(conversation_id);
CREATE INDEX idx_message_files_workspace_id ON chat.message_files(workspace_id);
