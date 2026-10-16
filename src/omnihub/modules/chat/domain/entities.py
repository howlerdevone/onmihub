from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Conversation:
  id: UUID
  workspace_id: UUID
  user_id: UUID
  title: str
  created_at: datetime
  updated_at: datetime


@dataclass
class Message:
  id: UUID
  conversation_id: UUID
  sender: str  # 'user', 'bot', 'system'
  source: str  # 'web', 'whatsapp', 'telegram'
  content: str
  created_at: datetime


@dataclass
class MessageFile:
  id: UUID
  message_id: UUID
  conversation_id: UUID
  workspace_id: UUID
  filename: str
  gcs_path: str
  created_at: datetime
