from contextvars import ContextVar


ctx_data = ContextVar("command_ctx_data")
current_message = ContextVar("current_ctx_message")
