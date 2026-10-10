from __future__ import annotations

import asyncio
import json
from typing import Any

from google.cloud import storage
from google.cloud.storage import Client


class GcsClient:
  """
  Low-level wrapper over google-cloud-storage SDK.
  Provides async-friendly interface by wrapping blocking calls in asyncio.to_thread().
  """

  def __init__(self, credentials_json: str, bucket_name: str):
    """
    Initialize GCS client from service account JSON string and bucket name.

    Args:
      credentials_json: Raw JSON string containing service account credentials.
      bucket_name: Name of the GCS bucket to operate on.
    """
    credentials_info: dict[str, Any] = json.loads(credentials_json)
    self._client: Client = storage.Client.from_service_account_info(credentials_info)
    self._bucket_name = bucket_name

  async def create_folder(self, path: str) -> None:
    """
    Create a folder marker (empty blob with trailing slash) at the given path.

    Args:
      path: The folder path (e.g., "workspace-id/user-id"). Trailing slash added if missing.
    """
    folder_key = path if path.endswith("/") else f"{path}/"
    blob = self._client.bucket(self._bucket_name).blob(folder_key)
    await asyncio.to_thread(blob.upload_from_string, b"")

  async def list_blobs(self, prefix: str) -> list[storage.Blob]:
    """
    List all blobs under the given prefix.

    Args:
      prefix: Object key prefix to filter by.

    Returns:
      List of Blob objects matching the prefix.
    """
    return await asyncio.to_thread(lambda: list(self._client.list_blobs(self._bucket_name, prefix=prefix)))

  async def get_blob_bytes(self, path: str) -> bytes:
    """
    Download a blob's contents as bytes.

    Args:
      path: The object key path.

    Returns:
      Blob contents as bytes.

    Raises:
      google.cloud.exceptions.NotFound: If the blob does not exist.
    """
    blob = self._client.bucket(self._bucket_name).blob(path)
    return await asyncio.to_thread(blob.download_as_bytes)
