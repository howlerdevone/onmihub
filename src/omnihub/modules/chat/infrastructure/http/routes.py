from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, status

from omnihub.modules.auth.dependencies.auth_guard import get_auth_session
from omnihub.modules.auth.domain.entities import AuthSession
from omnihub.modules.chat.application.service import ChatApplicationService
from omnihub.modules.chat.dependencies.chat_dependency import get_chat_service
from omnihub.modules.chat.infrastructure.http.schemas import (
  ConversationResponse,
  CreateConversationRequest,
  CreateMessageRequest,
  ListConversationsResponse,
  ListMessagesResponse,
  MessageFileResponse,
  UploadMessageFilesResponse,
)


router = APIRouter(prefix="/v1/chat", tags=["chat"])


@router.post(
  "/conversations",
  response_model=ConversationResponse,
  status_code=status.HTTP_201_CREATED,
)
async def create_conversation(
  workspace_id: UUID,
  body: CreateConversationRequest,
  auth_session: AuthSession = Depends(get_auth_session),
  chat_service: ChatApplicationService = Depends(get_chat_service),
):
  """Create a new conversation in a workspace."""
  return await chat_service.create_conversation(
    workspace_id=workspace_id,
    user_id=auth_session.user_id,
    title=body.title,
  )


@router.get("/conversations", response_model=ListConversationsResponse)
async def list_conversations(
  workspace_id: UUID,
  auth_session: AuthSession = Depends(get_auth_session),
  chat_service: ChatApplicationService = Depends(get_chat_service),
):
  """List all conversations for the authenticated user in a workspace."""
  conversations = await chat_service.list_conversations(
    workspace_id=workspace_id,
    user_id=auth_session.user_id,
  )
  return ListConversationsResponse(conversations=conversations)


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
  conversation_id: UUID,
  auth_session: AuthSession = Depends(get_auth_session),
  chat_service: ChatApplicationService = Depends(get_chat_service),
):
  """Fetch a specific conversation."""
  return await chat_service.get_conversation(
    conversation_id=conversation_id,
    user_id=auth_session.user_id,
  )


@router.post(
  "/conversations/{conversation_id}/messages",
  status_code=status.HTTP_201_CREATED,
)
async def create_message(
  workspace_id: UUID,
  conversation_id: UUID,
  body: CreateMessageRequest,
  auth_session: AuthSession = Depends(get_auth_session),
  chat_service: ChatApplicationService = Depends(get_chat_service),
):
  """Create a message in a conversation and trigger an agent run."""
  return await chat_service.execute_create_message_with_run(
    workspace_id=workspace_id,
    user_id=auth_session.user_id,
    conversation_id=conversation_id,
    content=body.message,
    source=body.source,
  )


@router.get(
  "/conversations/{conversation_id}/messages",
  response_model=ListMessagesResponse,
)
async def list_messages(
  conversation_id: UUID,
  limit: int = 50,
  auth_session: AuthSession = Depends(get_auth_session),
  chat_service: ChatApplicationService = Depends(get_chat_service),
):
  """List messages in a conversation."""
  messages = await chat_service.list_messages(
    conversation_id=conversation_id,
    limit=limit,
  )
  return ListMessagesResponse(messages=messages)


@router.post(
  "/conversations/{conversation_id}/messages/{message_id}/files",
  response_model=UploadMessageFilesResponse,
  status_code=status.HTTP_201_CREATED,
)
async def upload_message_files(
  workspace_id: UUID,
  conversation_id: UUID,
  message_id: UUID,
  files: list[UploadFile] = File(...),
  auth_session: AuthSession = Depends(get_auth_session),
  chat_service: ChatApplicationService = Depends(get_chat_service),
):
  """Upload files to a message."""
  # Verify conversation belongs to user
  await chat_service.get_conversation(
    conversation_id=conversation_id,
    user_id=auth_session.user_id,
  )

  # Read files into memory
  file_list = []
  for upload_file in files:
    content = await upload_file.read()
    file_list.append((upload_file.filename or "file", content))

  # Upload all files
  uploaded_files = await chat_service.execute_upload_message_files(
    workspace_id=workspace_id,
    conversation_id=conversation_id,
    message_id=message_id,
    files=file_list,
  )

  return UploadMessageFilesResponse(
    message_id=message_id,
    files=[MessageFileResponse(**f) for f in uploaded_files],
  )
