from _contextvars import ContextVar

current_message = ContextVar("current_message")
ctx_data = ContextVar("ctx_data")
