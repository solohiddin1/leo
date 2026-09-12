import requests
from django.conf import settings
from concurrent.futures import ThreadPoolExecutor

from apps.shared.middleware.middleware import get_logger

logger = get_logger()
executor = ThreadPoolExecutor(max_workers=2)

class AdminTelegramNotifier:

    @staticmethod
    def send_heavy_request(url: str, data: dict):
        try:
            requests.post(url, json=data, timeout=10)
        except Exception as exc:
            logger.warning(f"Background HTTP request failed: {exc}")


    @classmethod
    def send(cls, text: str) -> None:
        if not settings.TELEGRAM_ADMIN_BOT_TOKEN or not settings.TELEGRAM_ADMIN_CHAT_ID:
            return
        try:
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_ADMIN_BOT_TOKEN}/sendMessage"
            json={"chat_id": settings.TELEGRAM_ADMIN_CHAT_ID, "text": text}
            executor.submit(cls.send_heavy_request, url, data=json)
            logger.info(f"Notified admin telegram chat: {text}")
        except Exception as exc:
            logger.warning(f"Failed to notify admin telegram chat: {exc}")
