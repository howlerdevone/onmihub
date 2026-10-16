import secrets
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID

from omnihub.config.settings import (
  AGENT_HEARTBEAT_INTERVAL_SECONDS,
  AGENT_LOCALE,
  AGENT_MAX_COST_USD,
  AGENT_MAX_OUTPUT_BYTES,
  AGENT_MAX_TURNS,
  AGENT_SYSTEM_PROMPT,
  AGENT_TIMEOUT_SECONDS,
  AGENT_TIMEZONE,
  ANTHROPIC_API_KEY,
  API_BASE_URL,
  DEFAULT_MODEL_ID,
)
from omnihub.modules.agents.domain.entities import Run
from omnihub.modules.agents.infrastructure.database.agent_credentials_adapter import AgentCredentialsAdapter
from omnihub.modules.agents.ports.runs_provider_port import RunsProviderPort


if TYPE_CHECKING:
  from omnihub.modules.agents.ports.agent_event_port import AgentEventPort


class AgentsApplicationService:
  """Application service for agent run workflows."""

  def __init__(
    self,
    runs_provider: RunsProviderPort,
    credentials_adapter: AgentCredentialsAdapter,
    event_provider: "AgentEventPort | None" = None,
  ) -> None:
    self.runs_provider = runs_provider
    self.credentials_adapter = credentials_adapter
    self.event_provider = event_provider

  def _build_manifest(
    self,
    *,
    workspace_id: UUID,
    conversation_id: UUID,
    message_content: str,
    message_source: str,
    app_credentials: list[dict[str, Any]] | None = None,
  ) -> dict[str, Any]:
    """Build agent manifest with configuration from environment."""
    return {
      "workspaceId": str(workspace_id),
      "conversationId": str(conversation_id),
      "createdAt": datetime.now(UTC).isoformat(),
      "agent": {
        "version": "2026-10-01.1",
        "systemPrompt": AGENT_SYSTEM_PROMPT,
        "locale": AGENT_LOCALE,
        "timezone": AGENT_TIMEZONE,
      },
      "input": {
        "message": message_content,
        "source": message_source,
        "history": [],
        "files": [],
      },
      "model": {
        "provider": "anthropic",
        "modelId": DEFAULT_MODEL_ID,
      },
      "apps": [
        {
          "appId": app["app_id"],
          "name": app["app_name"],
          "mcpUrl": app["mcp_url"],
          "auth": app.get("credentials", {}),
          "tools": [],
        }
        for app in (app_credentials or [])
      ],
      "limits": {
        "maxTurns": AGENT_MAX_TURNS,
        "maxCostUsd": AGENT_MAX_COST_USD,
        "timeoutSeconds": AGENT_TIMEOUT_SECONDS,
        "maxOutputBytes": AGENT_MAX_OUTPUT_BYTES,
      },
      "tools": {"bash": False, "allowedMcpTools": "per-app"},
      "permissionMode": "acceptEdits",
      "callbacks": {
        "eventsUrl": f"{API_BASE_URL}/v1/agents/runs/{{runId}}/events",
        "completeUrl": f"{API_BASE_URL}/v1/agents/runs/{{runId}}/complete",
        "heartbeatIntervalSeconds": AGENT_HEARTBEAT_INTERVAL_SECONDS,
      },
    }

  async def execute_create_run_for_conversation(
    self,
    *,
    workspace_id: UUID,
    user_id: UUID,
    conversation_id: UUID,
    message_id: UUID,
    message_content: str,
    message_source: str = "web",
  ) -> Run:
    """Create a new agent run from a conversation message with complete manifest."""
    run_token = secrets.token_urlsafe(32)

    manifest = self._build_manifest(
      workspace_id=workspace_id,
      conversation_id=conversation_id,
      message_content=message_content,
      message_source=message_source,
    )

    return await self.execute_create_run(
      workspace_id=workspace_id,
      user_id=user_id,
      conversation_id=conversation_id,
      message_id=message_id,
      manifest=manifest,
      run_token=run_token,
    )

  async def execute_create_run(
    self,
    *,
    workspace_id: UUID,
    user_id: UUID,
    conversation_id: UUID,
    message_id: UUID,
    manifest: dict[str, Any],
    run_token: str,
  ) -> Run:
    """Create a new agent run."""
    return await self.runs_provider.create_run(
      workspace_id=workspace_id,
      user_id=user_id,
      conversation_id=conversation_id,
      message_id=message_id,
      manifest=manifest,
      run_token=run_token,
    )

  async def get_run(
    self,
    *,
    run_id: UUID,
    run_token: str,
  ) -> Run:
    """Fetch a run and validate the access token."""
    return await self.runs_provider.get_run(run_id=run_id, run_token=run_token)

  async def execute_get_manifest_with_credentials(
    self,
    *,
    run_id: UUID,
    user_id: UUID,
    run_token: str,
  ) -> dict[str, Any]:
    """Fetch manifest and inject credentials from database."""
    run = await self.runs_provider.get_run(run_id=run_id, run_token=run_token)
    manifest = run.manifest.copy()

    # Add runId to manifest
    manifest["runId"] = str(run_id)

    # Fetch app credentials for this run's user and workspace
    app_credentials = await self.credentials_adapter.get_workspace_app_credentials(
      workspace_id=UUID(manifest["workspaceId"]),
      user_id=run.user_id,
    )

    # Build a lookup map for easy access
    credentials_map = {str(app["app_id"]): app for app in app_credentials}

    # Inject credentials into apps
    if "apps" in manifest:
      for app in manifest["apps"]:
        app_id = app.get("appId")
        if app_id in credentials_map:
          creds = credentials_map[app_id]
          # Inject plaintext credentials (MVP)
          app["auth"] = creds.get("credentials", {})

    # Inject API key for model
    manifest["model"]["apiKey"] = ANTHROPIC_API_KEY

    return manifest

  async def list_queued_runs(self) -> list[Run]:
    """List all queued runs for the dispatcher."""
    return await self.runs_provider.list_queued_runs()

  async def update_run_status(
    self,
    *,
    run_id: UUID,
    status: str,
    last_seq: int | None = None,
    usage: dict[str, Any] | None = None,
  ) -> Run:
    """Update run status with optional final seq and usage."""
    return await self.runs_provider.update_run_status(
      run_id=run_id,
      status=status,
      last_seq=last_seq,
      usage=usage,
    )

  async def execute_record_events(
    self,
    *,
    run_id: UUID,
    events: list[Any],
  ) -> None:
    """Record batch of events for audit trail."""
    if self.event_provider:
      for event in events:
        event_data = {"seq": event.seq}
        if event.data:
          event_data.update(event.data)

        await self.event_provider.create_event(
          run_id=run_id,
          event_type=event.type,
          data=event_data,
        )

  async def execute_generate_signed_url_for_file(
    self,
    *,
    run_id: UUID,
    filename: str,
  ) -> dict[str, str]:
    """Generate signed URL for direct file upload to GCS."""
    from omnihub.gateway.gcs_storage import get_gcs_client
    from omnihub.modules.agents.infrastructure.http.schemas import FileUploadResponse

    file_id = f"f_{secrets.token_hex(8)}"
    gcs_path = f"runs/{run_id}/{file_id}_{filename}"

    gcs_client = get_gcs_client()
    signed_url = await gcs_client.generate_signed_url(gcs_path, method="PUT")

    return FileUploadResponse(file_id=file_id, signed_url=signed_url).model_dump()
