from fastapi import APIRouter, status


router = APIRouter(tags=["Operations"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> dict[str, str]:
  """
  Liveness probe for the hosting platform. Deliberately free of any external
  dependency (database, authentication, storage) so that an outage in one of them
  never makes an otherwise healthy process look dead to the load balancer.
  """
  return {"status": "ok"}
