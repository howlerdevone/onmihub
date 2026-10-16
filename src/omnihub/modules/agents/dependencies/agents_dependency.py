from uuid import UUID

from fastapi import Depends, Header, HTTPException, Request, status

from omnihub.common.db.pg_client import PgClient
from omnihub.modules.agents.application.service import AgentsApplicationService
from omnihub.modules.agents.domain.entities import Run
from omnihub.modules.agents.infrastructure.database.agent_credentials_adapter import AgentCredentialsAdapter
from omnihub.modules.agents.infrastructure.database.agent_event_pg_adapter import AgentEventPgAdapter
from omnihub.modules.agents.infrastructure.database.runs_pg_adapter import RunsPgAdapter
from omnihub.modules.agents.ports.agent_event_port import AgentEventPort
from omnihub.modules.agents.ports.runs_provider_port import RunsProviderPort
from omnihub.modules.auth.dependencies.auth_guard import get_authenticated_user_id


def get_runs_provider(request: Request) -> RunsProviderPort:
  """Return the current runs provider implementation."""
  db_client: PgClient = request.state.db_client
  return RunsPgAdapter(db=db_client)


def get_credentials_adapter(request: Request) -> AgentCredentialsAdapter:
  """Return the agent credentials adapter."""
  db_client: PgClient = request.state.db_client
  return AgentCredentialsAdapter(db=db_client)


def get_event_provider(request: Request) -> AgentEventPort:
  """Return the current agent event provider implementation."""
  db_client: PgClient = request.state.db_client
  return AgentEventPgAdapter(db=db_client)


async def get_agents_service(
  runs_provider: RunsProviderPort = Depends(get_runs_provider),
  credentials_adapter: AgentCredentialsAdapter = Depends(get_credentials_adapter),
  event_provider: AgentEventPort = Depends(get_event_provider),
) -> AgentsApplicationService:
  """Composition root for agent workflows using runs and event providers."""
  return AgentsApplicationService(
    runs_provider=runs_provider,
    credentials_adapter=credentials_adapter,
    event_provider=event_provider,
  )


async def get_authenticated_run(
  run_id: UUID,
  x_run_token: str = Header(...),
  user_id: UUID = Depends(get_authenticated_user_id),
  agents_service: AgentsApplicationService = Depends(get_agents_service),
) -> Run:
  """Validate X-Run-Token + user_id and return the run."""
  runs_provider = agents_service.runs_provider
  run = await runs_provider.get_run(run_id=run_id, run_token=x_run_token)

  if run.user_id != user_id:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail={
        "message": "User cannot access this run",
        "code": "RUN_ACCESS_DENIED",
      },
    )

  return run
