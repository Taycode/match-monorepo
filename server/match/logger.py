import logging
import structlog
from structlog.contextvars import merge_contextvars
from structlog.dev import ConsoleRenderer
from structlog.processors import (
    TimeStamper,
    add_log_level,
    CallsiteParameter,
    CallsiteParameterAdder,
    JSONRenderer,
    dict_tracebacks,
)


def configure_logging(env="development", log_format="console"):
    """Configures structured logging for the application."""
    processors = [
        merge_contextvars,  # Add thread-local context vars
        TimeStamper(fmt="iso"),  # Add ISO 8601 timestamp
        add_log_level,  # Include log level
        CallsiteParameterAdder(
            [
                CallsiteParameter.PATHNAME,
                CallsiteParameter.FUNC_NAME,
                CallsiteParameter.MODULE,
                CallsiteParameter.LINENO,
            ]
        ),  # Add call site details
        dict_tracebacks,  # Include tracebacks for exceptions
    ]

    if log_format == "console":
        # pass
        processors.append(ConsoleRenderer(colors=True))  # Dev logs
    elif log_format == "json":
        processors.append(JSONRenderer())  # Prod logs

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        level=logging.DEBUG if env == "development" else logging.INFO,
        format="%(message)s",
        handlers=[logging.StreamHandler()],
    )
