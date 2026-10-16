-- Add user_id to chat.conversations for tracking who initiated each conversation
ALTER TABLE chat.conversations
ADD COLUMN user_id UUID NOT NULL REFERENCES identity.users(id) ON DELETE CASCADE;

CREATE INDEX idx_conversations_user_id ON chat.conversations(user_id);
