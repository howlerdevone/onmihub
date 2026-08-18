-- migrate:up
CREATE SCHEMA IF NOT EXISTS communication;
CREATE SCHEMA IF NOT EXISTS chat;

-- --- 1. ENUMS DEFINITIONS ---

-- Strict enumeration for supported chat messaging systems
CREATE TYPE chat.message_sender_enum AS ENUM ('user', 'bot', 'system');

-- Strict classification of incoming traffic sources
CREATE TYPE chat.message_source_enum AS ENUM ('web', 'whatsapp', 'telegram');


-- --- 2. VERIFICATION & ROUTING (COMMUNICATION SCHEMA) ---

-- Maps physical phone numbers or chat IDs to internal User IDs
CREATE TABLE communication.channels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES identity.users(id) ON DELETE CASCADE,

    platform VARCHAR(30) NOT NULL,               -- 'whatsapp' or 'telegram'
    platform_chat_id VARCHAR(100) NOT NULL,       -- External identifier (e.g. '50688888888' or telegram internal integer)

    verification_code VARCHAR(10),               -- Temporal 6-digit challenge code (e.g., '482910')
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Restrictions: One user can only link one channel per platform.
    -- One phone number/chat ID can only belong to a single user in the entire system.
    CONSTRAINT unique_user_platform_channel UNIQUE (user_id, platform),
    CONSTRAINT unique_platform_chat_identity UNIQUE (platform, platform_chat_id)
);


-- --- 3. CONVERSATIONAL MEMORY ENGINE (CHAT SCHEMA) ---

-- Master session containers for context isolation
CREATE TABLE chat.conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES organizations.workspaces(id) ON DELETE CASCADE, -- Bound to workspace for data containment

    title VARCHAR(255) NOT NULL DEFAULT 'New Conversation',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Granular historical stream of conversational messages
CREATE TABLE chat.messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES chat.conversations(id) ON DELETE CASCADE,

    sender chat.message_sender_enum NOT NULL,     -- 'user', 'bot', or 'system'
    source chat.message_source_enum NOT NULL DEFAULT 'web', -- Tracks where the message came from
    content TEXT NOT NULL,                        -- The literal textual message payload

    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- --- 4. HIGH-PERFORMANCE WEBHOOK INDEXING ---

-- Critical index for webhook routing: Finds verified users instantly by phone/telegram ID
CREATE INDEX idx_communication_channels_webhook_lookup
ON communication.channels (platform, platform_chat_id)
WHERE is_verified = TRUE;

-- Critical index for AI memory stream: Pulls messages in strict chronological sequence
CREATE INDEX idx_chat_messages_chronological_sequence
ON chat.messages (conversation_id, created_at ASC);

-- migrate:down
DROP TABLE IF EXISTS chat.messages;
DROP TABLE IF EXISTS chat.conversations;
DROP TYPE IF EXISTS chat.message_source_enum;
DROP TYPE IF EXISTS chat.message_sender_enum;
DROP TABLE IF EXISTS communication.channels;
DROP SCHEMA IF EXISTS chat;
DROP SCHEMA IF EXISTS communication;
