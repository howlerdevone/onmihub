from datetime import datetime
from uuid import UUID

from omnihub.common.base_models import CustomBaseModel


class ConversationResponse(CustomBaseModel):
  id: UUID
  workspace_id: UUID
  user_id: UUID
  title: str
  created_at: datetime
  updated_at: datetime


class MessageResponse(CustomBaseModel):
  id: UUID
  conversation_id: UUID
  sender: str
  source: str
  content: str
  created_at: datetime


class MessageFileResponse(CustomBaseModel):
  id: UUID
  message_id: UUID
  filename: str
  gcs_path: str
  created_at: datetime


class CreateConversationRequest(CustomBaseModel):
  title: str = "New Conversation"


class CreateMessageRequest(CustomBaseModel):
  message: str
  source: str = "web"


class ListConversationsResponse(CustomBaseModel):
  conversations: list[ConversationResponse]


class ListMessagesResponse(CustomBaseModel):
  messages: list[MessageResponse]


class UploadMessageFilesResponse(CustomBaseModel):
  message_id: UUID
  files: list[MessageFileResponse]


class CreateMessageWithRunResponse(CustomBaseModel):
  message_id: UUID
  run_id: UUID | None = None
  run_status: str | None = None
