from uuid import UUID

from omnihub.common.db.pg_client import PgClient
from omnihub.modules.chat.domain.entities import Conversation, Message, MessageFile
from omnihub.modules.chat.domain.exceptions import (
  ConversationCreationError,
  ConversationNotFoundError,
  MessageCreationError,
)
from omnihub.modules.chat.ports.chat_provider_port import ChatProviderPort


class ChatPgAdapter(ChatProviderPort):
  """PostgreSQL implementation of the chat provider port."""

  def __init__(self, db: PgClient):
    self.db = db

  async def create_conversation(
    self,
    *,
    workspace_id: UUID,
    user_id: UUID,
    title: str,
  ) -> Conversation:
    """Create a new conversation."""
    row = await self.db.fetchrow(
      """
      INSERT INTO chat.conversations (workspace_id, user_id, title)
      VALUES ($1, $2, $3)
      RETURNING id, workspace_id, user_id, title, created_at, updated_at
      """,
      workspace_id,
      user_id,
      title,
    )

    if not row:
      raise ConversationCreationError("Failed to create conversation")

    return Conversation(
      id=row["id"],
      workspace_id=row["workspace_id"],
      user_id=row["user_id"],
      title=row["title"],
      created_at=row["created_at"],
      updated_at=row["updated_at"],
    )

  async def get_conversation(
    self,
    *,
    conversation_id: UUID,
    user_id: UUID,
  ) -> Conversation:
    """Fetch a conversation and verify ownership."""
    row = await self.db.fetchrow(
      """
      SELECT id, workspace_id, user_id, title, created_at, updated_at
      FROM chat.conversations
      WHERE id = $1 AND user_id = $2
      """,
      conversation_id,
      user_id,
    )

    if not row:
      raise ConversationNotFoundError("Conversation not found or access denied")

    return Conversation(
      id=row["id"],
      workspace_id=row["workspace_id"],
      user_id=row["user_id"],
      title=row["title"],
      created_at=row["created_at"],
      updated_at=row["updated_at"],
    )

  async def list_conversations(
    self,
    *,
    workspace_id: UUID,
    user_id: UUID,
  ) -> list[Conversation]:
    """List all conversations for a user in a workspace."""
    rows = await self.db.fetch(
      """
      SELECT id, workspace_id, user_id, title, created_at, updated_at
      FROM chat.conversations
      WHERE workspace_id = $1 AND user_id = $2
      ORDER BY updated_at DESC
      """,
      workspace_id,
      user_id,
    )

    return [
      Conversation(
        id=row["id"],
        workspace_id=row["workspace_id"],
        user_id=row["user_id"],
        title=row["title"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
      )
      for row in rows
    ]

  async def create_message(
    self,
    *,
    conversation_id: UUID,
    sender: str,
    source: str,
    content: str,
  ) -> Message:
    """Create a message in a conversation."""
    row = await self.db.fetchrow(
      """
      INSERT INTO chat.messages (conversation_id, sender, source, content)
      VALUES ($1, $2::chat.message_sender, $3::chat.message_source, $4)
      RETURNING id, conversation_id, sender, source, content, created_at
      """,
      conversation_id,
      sender,
      source,
      content,
    )

    if not row:
      raise MessageCreationError("Failed to create message")

    return Message(
      id=row["id"],
      conversation_id=row["conversation_id"],
      sender=row["sender"],
      source=row["source"],
      content=row["content"],
      created_at=row["created_at"],
    )

  async def list_messages(
    self,
    *,
    conversation_id: UUID,
    limit: int = 50,
  ) -> list[Message]:
    """List messages in a conversation."""
    rows = await self.db.fetch(
      """
      SELECT id, conversation_id, sender, source, content, created_at
      FROM chat.messages
      WHERE conversation_id = $1
      ORDER BY created_at DESC
      LIMIT $2
      """,
      conversation_id,
      limit,
    )

    return [
      Message(
        id=row["id"],
        conversation_id=row["conversation_id"],
        sender=row["sender"],
        source=row["source"],
        content=row["content"],
        created_at=row["created_at"],
      )
      for row in reversed(rows)
    ]

  async def list_messages_with_files(
    self,
    *,
    conversation_id: UUID,
    limit: int = 50,
  ) -> list[tuple[Message, list[MessageFile]]]:
    """List messages with their associated files."""
    rows = await self.db.fetch(
      """
      SELECT
        m.id, m.conversation_id, m.sender, m.source, m.content, m.created_at,
        f.id as file_id, f.filename, f.gcs_path, f.workspace_id, f.created_at as file_created_at
      FROM chat.messages m
      LEFT JOIN chat.message_files f ON f.message_id = m.id
      WHERE m.conversation_id = $1
      ORDER BY m.created_at DESC, f.created_at ASC
      LIMIT $2
      """,
      conversation_id,
      limit,
    )

    messages_dict: dict[UUID, tuple[Message, list[MessageFile]]] = {}
    for row in rows:
      msg_id = row["id"]
      if msg_id not in messages_dict:
        message = Message(
          id=row["id"],
          conversation_id=row["conversation_id"],
          sender=row["sender"],
          source=row["source"],
          content=row["content"],
          created_at=row["created_at"],
        )
        messages_dict[msg_id] = (message, [])

      if row["file_id"]:
        file = MessageFile(
          id=row["file_id"],
          message_id=msg_id,
          conversation_id=row["conversation_id"],
          workspace_id=row["workspace_id"],
          filename=row["filename"],
          gcs_path=row["gcs_path"],
          created_at=row["file_created_at"],
        )
        messages_dict[msg_id][1].append(file)

    return list(reversed(list(messages_dict.values())))
