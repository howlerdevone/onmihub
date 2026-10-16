from typing import TYPE_CHECKING

from fastapi import Depends, Request

from omnihub.common.db.pg_client import PgClient
from omnihub.modules.chat.application.service import ChatApplicationService
from omnihub.modules.chat.infrastructure.database.chat_pg_adapter import ChatPgAdapter
from omnihub.modules.chat.ports.chat_provider_port import ChatProviderPort
from omnihub.modules.storage.dependencies.storage_dependency import get_storage_service


if TYPE_CHECKING:
  from omnihub.modules.agents.application.service import AgentsApplicationService
  from omnihub.modules.storage.application.service import StorageApplicationService


def get_chat_provider(request: Request) -> ChatProviderPort:
  """Return the current chat provider implementation."""
  db_client: PgClient = request.state.db_client
  return ChatPgAdapter(db=db_client)


async def get_chat_service(
  chat_provider: ChatProviderPort = Depends(get_chat_provider),
  agents_service: "AgentsApplicationService | None" = None,
  storage_service: "StorageApplicationService" = Depends(get_storage_service),
) -> ChatApplicationService:
  """Composition root for chat workflows using the chat provider."""
  return ChatApplicationService(
    chat_provider=chat_provider,
    agents_service=agents_service,
    storage_service=storage_service,
  )
