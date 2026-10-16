from supabase import AsyncClient, acreate_client

from omnihub.config.settings import SUPABASE_ANON_KEY, SUPABASE_URL


async def get_supabase_client() -> AsyncClient:
  """
  Infrastructure factory utility to instantiate and retrieve the official
  Supabase client SDK using strict validated environment variables boundary.
  """
  if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise RuntimeError(
      "CRITICAL INFRASTRUCTURE FAILURE: SUPABASE_URL and SUPABASE_ANON_KEY "
      "must be properly set in your environment configuration parameters."
    )

  return await acreate_client(SUPABASE_URL, SUPABASE_ANON_KEY)
