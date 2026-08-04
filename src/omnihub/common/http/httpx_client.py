from types import TracebackType
from typing import Any

import httpx

from omnihub.common.exceptions.http_error import HttpError


class HttpxClient:
  def __init__(self, base_url: str, headers: dict[str, str], cookies: dict[str, str]):
    self.client = httpx.AsyncClient(base_url=base_url, headers=headers, cookies=cookies)

  async def __aenter__(self):
    await self.client.__aenter__()
    return self

  async def __aexit__(
    self,
    exc_type: type[BaseException] | None,
    exc_val: BaseException | None,
    exc_tb: TracebackType | None,
  ) -> None:
    await self.client.__aexit__(exc_type, exc_val, exc_tb)

  async def post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
    response = await self.client.post(path, json=body)
    self._handle_response(response)
    return response.json()

  async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    response = await self.client.get(path, params=params)
    self._handle_response(response)
    return response.json()

  def _handle_response(self, response: httpx.Response) -> None:
    if response.status_code >= 400:
      raise HttpError(status_code=response.status_code, message=response.text)
