import logging
import os
import re
import threading
import time
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

DEFAULT_TIMEZONE_NAME = "Asia/Bangkok"
DEFAULT_UTC_OFFSET_HOURS = 7


class TelegramHeartbeatFilter(logging.Filter):
    """Convert noisy Telegram long-poll httpx logs into a readable heartbeat."""

    _pattern = re.compile(
        r"HTTP Request:\s+(GET|POST)\s+https://api\.telegram\.org/.+/getUpdates\b.*\b200 OK\b"
    )

    def __init__(self, min_interval_seconds=15):
        super().__init__()
        self._min_interval_seconds = max(0, int(min_interval_seconds))
        self._last_emit = 0.0
        self._lock = threading.Lock()

    def filter(self, record):
        message = record.getMessage()
        if not self._pattern.search(message):
            return True

        with self._lock:
            now = time.monotonic()
            if now - self._last_emit < self._min_interval_seconds:
                return False
            self._last_emit = now

        record.msg = "Telegram polling heartbeat: connection OK"
        record.args = ()
        return True


def configure_runtime_logging(heartbeat_interval_seconds=15):
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        )

    # Keep low-level transport logs quiet unless explicitly needed.
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    httpx_logger = logging.getLogger("httpx")
    has_filter = any(isinstance(f, TelegramHeartbeatFilter) for f in httpx_logger.filters)
    if not has_filter:
        httpx_logger.addFilter(TelegramHeartbeatFilter(heartbeat_interval_seconds))


def get_default_timezone_name():
    return os.environ.get("SSC_DEFAULT_TIMEZONE", DEFAULT_TIMEZONE_NAME)


def get_default_timezone():
    timezone_name = get_default_timezone_name()
    try:
        return ZoneInfo(timezone_name)
    except Exception:
        return timezone(
            timedelta(hours=DEFAULT_UTC_OFFSET_HOURS),
            name=f"UTC+{DEFAULT_UTC_OFFSET_HOURS:02d}:00",
        )


def _format_offset(delta):
    total_minutes = int(delta.total_seconds() // 60)
    sign = "+" if total_minutes >= 0 else "-"
    total_minutes = abs(total_minutes)
    hours, minutes = divmod(total_minutes, 60)
    return f"{sign}{hours:02d}:{minutes:02d}"


def initialize_default_timezone():
    timezone_name = get_default_timezone_name()
    if "TZ" not in os.environ:
        os.environ["TZ"] = timezone_name

    tzset_applied = False
    if hasattr(time, "tzset"):
        try:
            time.tzset()
            tzset_applied = True
        except Exception:
            tzset_applied = False

    tzinfo = get_default_timezone()
    now_local = datetime.now(tzinfo)
    offset = now_local.utcoffset() or timedelta(0)
    return {
        "timezone_name": timezone_name,
        "offset": _format_offset(offset),
        "tzset_applied": tzset_applied,
    }
