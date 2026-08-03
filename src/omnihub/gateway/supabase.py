import os

from supabase import Client, create_client

# Note: environment loading is intentionally performed at application startup
# (e.g. in `omnihub.cli`) to keep this module focused solely on Supabase
# client creation and to avoid side-effects during library import.


def get_supabase_client() -> Client:
    """
    Infrastructure factory utility to instantiate and retrieve the official
    Supabase client SDK using strict validated environment variables boundary.
    """
    supabase_url = os.environ.get("SUPABASE_URL")
    # Support both SUPABASE_KEY and SUPABASE_ANON_KEY variable names
    supabase_key = os.environ.get("SUPABASE_KEY") or os.environ.get("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        raise RuntimeError(
            "CRITICAL INFRASTRUCTURE FAILURE: SUPABASE_URL and SUPABASE_KEY "
            "must be properly set in your environment configuration parameters."
        )

    return create_client(supabase_url, supabase_key)
