from __future__ import annotations

from omnihub.common import CustomBaseModel


class AreaResponse(CustomBaseModel):
  id: str
  name: str


class AppResponse(CustomBaseModel):
  id: str
  name: str
  description: str | None = None
  icon_url: str | None = None
  url: str | None = None
