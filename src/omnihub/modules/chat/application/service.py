from typing import TYPE_CHECKING, Any
from uuid import UUID

from omnihub.modules.chat.domain.entities import Conversation, Message
from omnihub.modules.chat.ports.chat_provider_port import ChatProviderPort


if TYPE_CHECKING:
  from omnihub.modules.agents.application.service import AgentsApplicationService
  from omnihub.modules.storage.application.service import StorageApplicationService


class ChatApplicationService:
  """Application service for chat and conversation workflows."""

  def __init__(
    self,
    chat_provider: ChatProviderPort,
    agents_service: "AgentsApplicationService | None" = None,
    storage_service: "StorageApplicationService | None" = None,
  ) -> None:
    self.chat_provider = chat_provider
    self.agents_service = agents_service
    self.storage_service = storage_service

  async def create_conversation(
    self,
    *,
    workspace_id: UUID,
    user_id: UUID,
    title: str = "New Conversation",
  ) -> Conversation:
    """Create a new conversation in a workspace."""
    return await self.chat_provider.create_conversation(
      workspace_id=workspace_id,
      user_id=user_id,
      title=title,
    )

  async def get_conversation(
    self,
    *,
    conversation_id: UUID,
    user_id: UUID,
  ) -> Conversation:
    """Fetch a conversation and verify ownership."""
    return await self.chat_provider.get_conversation(
      conversation_id=conversation_id,
      user_id=user_id,
    )

  async def list_conversations(
    self,
    *,
    workspace_id: UUID,
    user_id: UUID,
  ) -> list[Conversation]:
    """List all conversations for a user in a workspace."""
    return await self.chat_provider.list_conversations(
      workspace_id=workspace_id,
      user_id=user_id,
    )

  async def create_message(
    self,
    *,
    conversation_id: UUID,
    sender: str,
    source: str,
    content: str,
  ) -> Message:
    """Create a message in a conversation."""
    return await self.chat_provider.create_message(
      conversation_id=conversation_id,
      sender=sender,
      source=source,
      content=content,
    )

  async def list_messages(
    self,
    *,
    conversation_id: UUID,
    limit: int = 50,
  ) -> list[Message]:
    """List messages in a conversation."""
    return await self.chat_provider.list_messages(
      conversation_id=conversation_id,
      limit=limit,
    )

  async def execute_create_message_with_run(
    self,
    *,
    workspace_id: UUID,
    user_id: UUID,
    conversation_id: UUID,
    content: str,
    source: str = "web",
  ) -> dict[str, Any]:
    """Create a message and trigger an agent run."""
    message = await self.create_message(
      conversation_id=conversation_id,
      sender="user",
      source=source,
      content=content,
    )

    run_id = None
    run_status = None
    if self.agents_service:
      run = await self.agents_service.execute_create_run_for_conversation(
        workspace_id=workspace_id,
        user_id=user_id,
        conversation_id=conversation_id,
        message_id=message.id,
        message_content=content,
        message_source=source,
      )
      run_id = run.id
      run_status = run.status

    return {
      "message_id": message.id,
      "run_id": run_id,
      "run_status": run_status,
    }

  async def execute_upload_message_files(
    self,
    *,
    workspace_id: UUID,
    conversation_id: UUID,
    message_id: UUID,
    files: list[tuple[str, bytes]],
  ) -> list[dict[str, Any]]:
    """Upload files for a message and create file records."""
    if not self.storage_service:
      raise RuntimeError("Storage service not available")

    uploaded_files = []
    for filename, file_content in files:
      # Upload to GCS
      gcs_path = f"{workspace_id}/{conversation_id}/{message_id}/{filename}"
      await self.storage_service.execute_upload_file(
        key=gcs_path,
        content=file_content,
      )

      # Create file record
      message_file = await self.chat_provider.create_message_file(
        message_id=message_id,
        conversation_id=conversation_id,
        workspace_id=workspace_id,
        filename=filename,
        gcs_path=gcs_path,
      )

      uploaded_files.append(
        {
          "id": str(message_file.id),
          "filename": message_file.filename,
          "gcs_path": message_file.gcs_path,
          "created_at": message_file.created_at.isoformat(),
        }
      )

    return uploaded_files
