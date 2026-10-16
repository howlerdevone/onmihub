class AgentException(Exception):
  pass


class RunNotFoundError(AgentException):
  pass


class RunCreationError(AgentException):
  pass


class RunAccessDeniedError(AgentException):
  pass


class InvalidRunTokenError(AgentException):
  pass
