import requests
from django.conf import settings

from apps.shared.middleware.middleware import get_logger

logger = get_logger()


class AdminTelegramNotifier:

    @classmethod
    def send(cls, text: str) -> None:
        if not settings.TELEGRAM_ADMIN_BOT_TOKEN or not settings.TELEGRAM_ADMIN_CHAT_ID:
            return
        try:
            requests.post(
                f"https://api.telegram.org/bot{settings.TELEGRAM_ADMIN_BOT_TOKEN}/sendMessage",
                json={"chat_id": settings.TELEGRAM_ADMIN_CHAT_ID, "text": text},
                timeout=10,
            )
        except Exception as exc:
            logger.warning(f"Failed to notify admin telegram chat: {exc}")
