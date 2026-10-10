import base64
import os
from pathlib import Path

from omnihub.common.storage import GcsClient


def get_gcs_client() -> GcsClient:
  """
  Infrastructure factory utility to instantiate and retrieve the GCS client
  using strict validated environment variables boundary.

  Supports two modes:
  1. File path: GOOGLE_APPLICATION_CREDENTIALS points to a JSON file
  2. Base64: GOOGLE_APPLICATION_CREDENTIALS contains base64-encoded JSON
  """
  credentials_input = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
  bucket_name = os.environ.get("BUCKET_NAME")

  if not credentials_input or not bucket_name:
    raise RuntimeError(
      "CRITICAL INFRASTRUCTURE FAILURE: GOOGLE_APPLICATION_CREDENTIALS and BUCKET_NAME "
      "must be properly set in your environment configuration parameters."
    )

  # Try to load from file path first
  credentials_path = Path(credentials_input)
  if credentials_path.exists() and credentials_path.is_file():
    try:
      credentials_json = credentials_path.read_text(encoding="utf-8")
    except Exception as error:
      raise RuntimeError(
        f"CRITICAL INFRASTRUCTURE FAILURE: Failed to read GOOGLE_APPLICATION_CREDENTIALS "
        f"from file path: {credentials_path}"
      ) from error
  else:
    # Fall back to base64 decoding
    try:
      credentials_json = base64.b64decode(credentials_input).decode("utf-8")
    except Exception as error:
      raise RuntimeError(
        "CRITICAL INFRASTRUCTURE FAILURE: Failed to decode GOOGLE_APPLICATION_CREDENTIALS "
        "as base64 or read as file path"
      ) from error

  return GcsClient(credentials_json=credentials_json, bucket_name=bucket_name)
