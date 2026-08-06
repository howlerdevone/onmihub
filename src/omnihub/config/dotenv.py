import os
from pathlib import Path


def load_dotenv_if_present(env_path: Path | None = None) -> None:
  """Load a .env file into os.environ if present.

  Fallback for local development when Doppler is not being used. In normal
  usage the `doppler-env` package (installed as a dev dep) runs a `.pth`
  hook at interpreter startup and, when DOPPLER_ENV=1 is set, populates
  os.environ from Doppler before this loader runs.

  - Only sets keys that are not already defined in the environment,
    so Doppler-injected values always win over `.env`.
  - Keeps implementation dependency-free (no python-dotenv required).
  - `env_path` defaults to project root `.env` (cwd / ".env").
  """
  env_path = Path.cwd() / ".env" if env_path is None else env_path
  if not env_path.exists():
    return

  for raw in env_path.read_text(encoding="utf-8").splitlines():
    line = raw.strip()
    if not line or line.startswith("#"):
      continue
    if "=" not in line:
      continue
    key, val = line.split("=", 1)
    key = key.strip()
    val = val.strip().strip("'\"")
    if key and key not in os.environ:
      os.environ[key] = val
