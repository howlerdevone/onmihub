from typing import Any, Protocol
from uuid import UUID

from omnihub.modules.chat.domain.entities import Conversation, Message


class ChatProviderPort(Protocol):
  """Architectural port defining chat persistence operations."""

  async def create_conversation(
    self,
    *,
    workspace_id: UUID,
    user_id: UUID,
    title: str,
  ) -> Conversation:
    """Create a new conversation."""
    ...

  async def get_conversation(
    self,
    *,
    conversation_id: UUID,
    user_id: UUID,
  ) -> Conversation:
    """Fetch a conversation and verify ownership."""
    ...

  async def list_conversations(
    self,
    *,
    workspace_id: UUID,
    user_id: UUID,
  ) -> list[Conversation]:
    """List all conversations for a user in a workspace."""
    ...

  async def create_message(
    self,
    *,
    conversation_id: UUID,
    sender: str,
    source: str,
    content: str,
  ) -> Message:
    """Create a message in a conversation."""
    ...

  async def list_messages(
    self,
    *,
    conversation_id: UUID,
    limit: int = 50,
  ) -> list[Message]:
    """List messages in a conversation in chronological order."""
    ...

  async def list_messages_with_files(
    self,
    *,
    conversation_id: UUID,
    limit: int = 50,
  ) -> list[tuple[Message, list[Any]]]:
    """List messages with their associated files."""
    ...

  async def create_message_file(
    self,
    *,
    message_id: UUID,
    conversation_id: UUID,
    workspace_id: UUID,
    filename: str,
    gcs_path: str,
  ) -> Any:
    """Create a file record for a message."""
    ...
