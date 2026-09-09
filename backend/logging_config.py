"""
Structured logging configuration supporting development (human-readable) and production (JSON) formats.
"""

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict

from backend.middleware.request_id import get_request_id


class StructuredJSONFormatter(logging.Formatter):
    """Formats log records as structured JSON for log aggregation (production)."""

    def format(self, record: logging.LogRecord) -> str:
        req_id = getattr(record, "request_id", None) or get_request_id()

        log_data: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": req_id,
            "extra": {},
        }

        # Format exception info if present
        if record.exc_info:
            log_data["extra"]["exception"] = self.formatException(record.exc_info)

        # Include extra attributes passed in log calls
        for key, val in record.__dict__.items():
            if key not in {
                "args", "asctime", "created", "exc_info", "exc_text", "filename",
                "funcName", "levelname", "levelno", "lineno", "module", "msecs",
                "message", "msg", "name", "pathname", "process", "processName",
                "relativeCreated", "stack_info", "thread", "threadName", "request_id",
            }:
                log_data["extra"][key] = str(val)

        return json.dumps(log_data)


class HumanReadableFormatter(logging.Formatter):
    """Formats log records with request_id tag for local development."""

    def format(self, record: logging.LogRecord) -> str:
        req_id = getattr(record, "request_id", None) or get_request_id()
        base_msg = super().format(record)
        return f"{base_msg} request_id={req_id}"


def setup_logging(log_level: str = "INFO", log_format: str = "human") -> None:
    """Configures application-wide logging handlers and formatters."""
    level = getattr(logging, log_level.upper(), logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)

    if log_format.lower() == "json":
        formatter = StructuredJSONFormatter()
    else:
        formatter = HumanReadableFormatter(
            fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s"
        )

    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)
