class ChatException(Exception):
  pass


class ConversationNotFoundError(ChatException):
  pass


class ConversationCreationError(ChatException):
  pass


class MessageNotFoundError(ChatException):
  pass


class MessageCreationError(ChatException):
  pass


class ChatAccessDeniedError(ChatException):
  pass
