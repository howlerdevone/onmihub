from typing import Any
from uuid import UUID

from omnihub.common.db.pg_client import PgClient


class AgentCredentialsAdapter:
  """Adapter for fetching workspace app credentials."""

  def __init__(self, db: PgClient):
    self.db = db

  async def get_workspace_app_credentials(
    self,
    *,
    workspace_id: UUID,
    user_id: UUID,
  ) -> list[dict[str, Any]]:
    """Fetch all app credentials for a user in a workspace."""
    rows = await self.db.fetch(
      """
      SELECT
        wac.app_id,
        a.name as app_name,
        a.url as mcp_url,
        a.mcp_auth_config_template,
        wac.credentials
      FROM organizations.workspace_app_credentials wac
      JOIN catalog.apps a ON a.id = wac.app_id
      WHERE wac.workspace_id = $1 AND wac.user_id = $2
      """,
      workspace_id,
      user_id,
    )

    return [
      {
        "app_id": row["app_id"],
        "app_name": row["app_name"],
        "mcp_url": row["mcp_url"],
        "auth_template": row["mcp_auth_config_template"],
        "credentials": row["credentials"],
      }
      for row in rows
    ]
