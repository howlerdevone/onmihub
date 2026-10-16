import os


# ─────────────────────────────────────────────
# Supabase (required)
# ─────────────────────────────────────────────
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")

# ─────────────────────────────────────────────
# Database (optional — defaults to local Docker)
# ─────────────────────────────────────────────
DATABASE_URL = os.environ.get(
  "DATABASE_URL",
  "postgres://omni_user:omni_password@localhost:5433/omnihub_dev",
)

# ─────────────────────────────────────────────
# Server (optional — defaults shown)
# ─────────────────────────────────────────────
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))
OMNIHUB_RELOAD = os.environ.get("OMNIHUB_RELOAD", "false").lower() == "true"

# ─────────────────────────────────────────────
# Redis (optional — for Celery task queue)
# ─────────────────────────────────────────────
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

# ─────────────────────────────────────────────
# Google Cloud Storage (required)
# ─────────────────────────────────────────────
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

# ─────────────────────────────────────────────
# Agent configuration
# ─────────────────────────────────────────────
AGENT_SYSTEM_PROMPT = os.environ.get(
  "AGENT_SYSTEM_PROMPT",
  "Eres un asistente que ayuda al usuario con sus tareas conectadas.",
)
AGENT_LOCALE = os.environ.get("AGENT_LOCALE", "es-CR")
AGENT_TIMEZONE = os.environ.get("AGENT_TIMEZONE", "America/Costa_Rica")
DEFAULT_MODEL_ID = os.environ.get("DEFAULT_MODEL_ID", "claude-sonnet-5")

# ─────────────────────────────────────────────
# Agent limits
# ─────────────────────────────────────────────
AGENT_MAX_TURNS = int(os.environ.get("AGENT_MAX_TURNS", "30"))
AGENT_MAX_COST_USD = float(os.environ.get("AGENT_MAX_COST_USD", "0.5"))
AGENT_TIMEOUT_SECONDS = int(os.environ.get("AGENT_TIMEOUT_SECONDS", "600"))
AGENT_MAX_OUTPUT_BYTES = int(os.environ.get("AGENT_MAX_OUTPUT_BYTES", "10485760"))
AGENT_HEARTBEAT_INTERVAL_SECONDS = int(os.environ.get("AGENT_HEARTBEAT_INTERVAL_SECONDS", "30"))

# ─────────────────────────────────────────────
# API Keys for LLM Providers (for agent execution)
# ─────────────────────────────────────────────
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# ─────────────────────────────────────────────
# API configuration
# ─────────────────────────────────────────────
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.omnihub.example")
