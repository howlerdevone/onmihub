from datetime import datetime
from typing import Any
from uuid import UUID

from omnihub.common.base_models import CustomBaseModel


class RunResponse(CustomBaseModel):
  id: UUID
  workspace_id: UUID
  user_id: UUID
  conversation_id: UUID
  message_id: UUID
  status: str
  run_token: str
  created_at: datetime
  completed_at: datetime | None = None


class CreateRunRequest(CustomBaseModel):
  conversation_id: UUID
  message_id: UUID


class CreateRunResponse(CustomBaseModel):
  run_id: UUID
  status: str


class ManifestResponse(CustomBaseModel):
  run_id: UUID
  workspace_id: UUID
  conversation_id: UUID
  agent: dict[str, Any]
  input: dict[str, Any]
  model: dict[str, Any]
  apps: list[dict[str, Any]]
  limits: dict[str, Any]
  tools: dict[str, Any]
  permission_mode: str
  callbacks: dict[str, Any]


class AgentEvent(CustomBaseModel):
  seq: int
  type: str  # 'message', 'tool.call', 'tool.result', 'file', etc.
  data: dict[str, Any] | None = None


class PostEventsRequest(CustomBaseModel):
  events: list[AgentEvent]


class PostEventsResponse(CustomBaseModel):
  status: str
  received_count: int


class FileUploadRequest(CustomBaseModel):
  filename: str


class FileUploadResponse(CustomBaseModel):
  file_id: str
  signed_url: str


class CompleteRunRequest(CustomBaseModel):
  status: str  # 'done', 'failed', 'blocked'
  last_seq: int
  usage: dict[str, Any] | None = None
  error: str | None = None


class RunStatusResponse(CustomBaseModel):
  status: str  # 'queued', 'running', 'done', 'failed', 'blocked', 'cancelled'
  cancelled: bool = False
