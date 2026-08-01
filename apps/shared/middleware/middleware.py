import datetime
import logging
import os
import json
from threading import Lock

from django.utils.deprecation import MiddlewareMixin

from root.settings import BASE_DIR

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

_logger = None
_logger_lock = Lock()


class DailyFileHandler(logging.FileHandler):
    KEEP_DAYS = 30

    def __init__(self):
        self._log_date = datetime.date.today()
        super().__init__(self._dated_path(self._log_date), encoding='utf-8')

    @staticmethod
    def _dated_path(date: datetime.date) -> str:
        return os.path.join(LOG_DIR, f"{date.strftime('%Y-%m-%d')}.log")

    def emit(self, record):
        today = datetime.date.today()
        if today != self._log_date:
            self.close()
            self._log_date = today
            self.baseFilename = os.path.abspath(self._dated_path(today))
            self.stream = self._open()
            self._cleanup_old_logs()
        super().emit(record)

    def _cleanup_old_logs(self):
        cutoff = datetime.date.today() - datetime.timedelta(days=self.KEEP_DAYS)
        try:
            for fname in os.listdir(LOG_DIR):
                if not fname.endswith('.log'):
                    continue
                date_part = fname[:-len('.log')]
                try:
                    if datetime.date.fromisoformat(date_part) < cutoff:
                        os.remove(os.path.join(LOG_DIR, fname))
                except ValueError:
                    pass
        except Exception:
            pass

SENSITIVE_KEYS = {"password", "token", "access", "refresh", "authorization", "otp", "secret"}

def redact_body(body: str) -> str:
    try:
        data = json.loads(body)
    except (ValueError, TypeError):
        return body

    def _redact(obj):
        if isinstance(obj, dict):
            return {
                k: ("***REDACTED***" if k.lower() in SENSITIVE_KEYS else _redact(v))
                for k, v in obj.items()
            }
        if isinstance(obj, list):
            return [_redact(i) for i in obj]
        return obj

    return json.dumps(_redact(data))

def get_logger():
    """Thread-safe singleton logger"""
    global _logger

    with _logger_lock:
        if _logger is None:
            _logger = logging.getLogger("daily_logger")
            _logger.setLevel(logging.INFO)
            _logger.handlers.clear()
            _logger.propagate = False

            handler = DailyFileHandler()
            formatter = logging.Formatter("[{asctime}] {levelname} {message}", style="{")
            handler.setFormatter(formatter)
            _logger.addHandler(handler)

    return _logger


def is_swagger_request(path: str) -> bool:
    return any([
        path.startswith("/swagger"),
        path.startswith("/redoc"),
        path.startswith("/openapi"),  # for drf-spectacular
    ])


def should_skip_logging(path: str) -> bool:
    return any([
        path.startswith("/api/v1/swagger"),
        path.startswith("/api/v1/redoc"),
        path.startswith("/api/v1/media/"),
        path.startswith("/api/v1/admin/"),
        path.startswith("/api/v1/user/login/"),
        path.startswith("/api/v1/user/set_password/"),
        path.startswith("/api/v1/static/"),
        path.startswith("/api/v1/favicon.ico")
    ])


class ExceptionMiddleware(MiddlewareMixin):
    """Logs any unhandled exception."""

    def process_exception(self, request, exception):
        if is_swagger_request(request.path):
            return None  # skip swagger errors

        logger = get_logger()
        logger.exception(exception)
        return None


class RequestResponseLoggingMiddleware(MiddlewareMixin):
    MAX_LOG_LENGTH = 500  # limit logged content size

    def process_request(self, request):
        if should_skip_logging(request.path):
            return None

        logger = get_logger()
        try:
            body = request.body.decode(errors="ignore")
        except Exception:
            body = "<unreadable body>"

        if len(body) > self.MAX_LOG_LENGTH:
            body = body[:self.MAX_LOG_LENGTH] + "... [truncated]"

        logger.info(
            f"REQUEST | {request.method} {request.get_full_path()} | Body: {body}"
        )

    def process_response(self, request, response):
        if should_skip_logging(request.path):
            return response

        logger = get_logger()

        content_type = response.get("Content-Type", "")
        if any(ct in content_type for ct in ["image", "pdf", "octet-stream"]):
            content = f"<binary content skipped: {content_type}>"
        else:
            try:
                content = response.content.decode(errors="ignore")
            except Exception:
                content = "<unreadable content>"

            if len(content) > self.MAX_LOG_LENGTH:
                content = content[:self.MAX_LOG_LENGTH] + "... [truncated]"

        logger.info(
            f"RESPONSE | {request.method} {request.get_full_path()} | "
            f"Status: {response.status_code} | Content: {content}"
        )
        return response
