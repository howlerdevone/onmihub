
from fastapi import APIRouter, Depends, status

from omnihub.modules.agents.application.service import AgentsApplicationService
from omnihub.modules.agents.dependencies.agents_dependency import (
  get_agents_service,
  get_authenticated_run,
)
from omnihub.modules.agents.domain.entities import Run
from omnihub.modules.agents.infrastructure.http.schemas import (
  CompleteRunRequest,
  FileUploadRequest,
  FileUploadResponse,
  PostEventsRequest,
  PostEventsResponse,
  RunStatusResponse,
)


router = APIRouter(prefix="/v1/agents", tags=["agents"])


@router.get("/runs/{run_id}/manifest")
async def get_manifest(
  run: Run = Depends(get_authenticated_run),
  agents_service: AgentsApplicationService = Depends(get_agents_service),
):
  """Fetch run manifest with credentials (validates JWT + run_token)."""
  return await agents_service.execute_get_manifest_with_credentials(
    run_id=run.id,
    user_id=run.user_id,
    run_token=run.run_token,
  )


@router.post("/runs/{run_id}/events", status_code=status.HTTP_202_ACCEPTED)
async def post_events(
  body: PostEventsRequest,
  run: Run = Depends(get_authenticated_run),
  agents_service: AgentsApplicationService = Depends(get_agents_service),
) -> PostEventsResponse:
  """Agent reports batch of events (validates JWT + run_token)."""
  await agents_service.execute_record_events(
    run_id=run.id,
    events=body.events,
  )

  return PostEventsResponse(status="received", received_count=len(body.events))


@router.post("/runs/{run_id}/files", status_code=status.HTTP_201_CREATED)
async def request_file_upload(
  body: FileUploadRequest,
  run: Run = Depends(get_authenticated_run),
  agents_service: AgentsApplicationService = Depends(get_agents_service),
) -> FileUploadResponse:
  """Request signed URL for direct file upload to GCS."""
  return await agents_service.execute_generate_signed_url_for_file(
    run_id=run.id,
    filename=body.filename,
  )


@router.get("/runs/{run_id}/status")
async def get_run_status(
  run: Run = Depends(get_authenticated_run),
) -> RunStatusResponse:
  """Check if run was cancelled."""
  return RunStatusResponse(
    status=run.status,
    cancelled=run.status == "cancelled",
  )


@router.post("/runs/{run_id}/complete", status_code=status.HTTP_200_OK)
async def complete_run(
  body: CompleteRunRequest,
  run: Run = Depends(get_authenticated_run),
  agents_service: AgentsApplicationService = Depends(get_agents_service),
):
  """Complete run with final seq and usage."""
  updated_run = await agents_service.update_run_status(
    run_id=run.id,
    status=body.status,
    last_seq=body.last_seq,
    usage=body.usage,
  )

  return {"status": updated_run.status}
