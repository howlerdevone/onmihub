import os

from omnihub.common.storage import GcsClient


def get_gcs_client() -> GcsClient:
  """
  Infrastructure factory utility to instantiate and retrieve the GCS client
  using strict validated environment variables boundary.
  """
  credentials_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
  bucket_name = os.environ.get("BUCKET_NAME")

  if not credentials_json or not bucket_name:
    raise RuntimeError(
      "CRITICAL INFRASTRUCTURE FAILURE: GOOGLE_APPLICATION_CREDENTIALS and BUCKET_NAME "
      "must be properly set in your environment configuration parameters."
    )

  return GcsClient(credentials_json=credentials_json, bucket_name=bucket_name)
