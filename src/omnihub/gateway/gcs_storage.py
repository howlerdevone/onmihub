import base64
import os
from pathlib import Path

from omnihub.common.storage import GcsClient


def get_gcs_client() -> GcsClient:
  """
  Infrastructure factory utility to instantiate and retrieve the GCS client
  using strict validated environment variables boundary.

  Supports four modes:
  1. File path: GOOGLE_APPLICATION_CREDENTIALS points to a JSON file
  2. Base64: GOOGLE_APPLICATION_CREDENTIALS contains base64-encoded JSON
  3. Inline: GCS_CREDENTIALS_JSON (or GOOGLE_APPLICATION_CREDENTIALS) holds a raw JSON object
  4. Unset: Application Default Credentials — the host's ambient identity, which on a
     managed runtime is the attached service account, so no key material is shipped
  """
  bucket_name = os.environ.get("BUCKET_NAME")

  if not bucket_name:
    raise RuntimeError(
      "CRITICAL INFRASTRUCTURE FAILURE: BUCKET_NAME must be properly set in your environment configuration parameters."
    )

  credentials_input = os.environ.get("GCS_CREDENTIALS_JSON") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

  return GcsClient(bucket_name=bucket_name, credentials_json=_resolve_credentials_json(credentials_input))


def _resolve_credentials_json(credentials_input: str | None) -> str | None:
  """
  Normalize a credentials variable into a service account JSON payload.

  Returns None when nothing is configured, which hands the decision to Application
  Default Credentials. A value that *is* configured but cannot be resolved raises:
  falling back to a different identity than the one asked for would hide the
  misconfiguration behind confusing permission errors later.
  """
  if not credentials_input:
    return None

  # An inline payload needs no further resolution.
  stripped = credentials_input.strip()
  if stripped.startswith("{"):
    return stripped

  # Try to load from file path first
  credentials_path = Path(credentials_input)
  if credentials_path.exists() and credentials_path.is_file():
    try:
      return credentials_path.read_text(encoding="utf-8")
    except OSError as error:
      raise RuntimeError(
        f"CRITICAL INFRASTRUCTURE FAILURE: Failed to read GOOGLE_APPLICATION_CREDENTIALS "
        f"from file path: {credentials_path}"
      ) from error

  # Fall back to base64 decoding
  try:
    return base64.b64decode(stripped, validate=True).decode("utf-8")
  except ValueError as error:
    raise RuntimeError(
      "CRITICAL INFRASTRUCTURE FAILURE: Failed to decode GOOGLE_APPLICATION_CREDENTIALS "
      "as base64, read as file path, or parse as inline JSON"
    ) from error
