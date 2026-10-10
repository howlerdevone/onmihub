"""
Business modules.

importing
any domain type load every router, which closed an import cycle between auth
and identity. Routers are registered explicitly in `omnihub.gateway.router`.
"""
