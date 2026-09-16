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

    @staticmethod
    def send_photo_request(url: str, data: dict, files: dict):
        try:
            requests.post(url, data=data, files=files, timeout=15)
        except Exception as exc:
            logger.warning(f"Background HTTP sendPhoto request failed: {exc}")

    @classmethod
    def send(cls, text: str) -> None:
        if not settings.TELEGRAM_ADMIN_BOT_TOKEN or not settings.TELEGRAM_ADMIN_CHAT_ID:
            return
        try:
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_ADMIN_BOT_TOKEN}/sendMessage"
            json = {"chat_id": settings.TELEGRAM_ADMIN_CHAT_ID, "text": text, "parse_mode": "HTML"}
            executor.submit(cls.send_heavy_request, url, data=json)
            logger.info(f"Notified admin telegram chat: {text}")
        except Exception as exc:
            logger.warning(f"Failed to notify admin telegram chat: {exc}")

    @classmethod
    def send_photo(cls, photo_file, caption: str = "") -> None:
        if not settings.TELEGRAM_ADMIN_BOT_TOKEN or not settings.TELEGRAM_ADMIN_CHAT_ID:
            return
        try:
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_ADMIN_BOT_TOKEN}/sendPhoto"
            data = {"chat_id": settings.TELEGRAM_ADMIN_CHAT_ID, "caption": caption, "parse_mode": "HTML"}

            file_content = None
            filename = "photo.jpg"

            if hasattr(photo_file, "path"):
                with open(photo_file.path, "rb") as f:
                    file_content = f.read()
                filename = photo_file.name.split("/")[-1]
            elif isinstance(photo_file, str):
                with open(photo_file, "rb") as f:
                    file_content = f.read()
                filename = photo_file.split("/")[-1]
            elif hasattr(photo_file, "read"):
                photo_file.seek(0)
                file_content = photo_file.read()
                if hasattr(photo_file, "name"):
                    filename = photo_file.name

            if not file_content:
                return

            files = {"photo": (filename, file_content, "image/jpeg")}
            executor.submit(cls.send_photo_request, url, data=data, files=files)
            logger.info(f"Sent photo to admin telegram chat: {caption}")
        except Exception as exc:
            logger.warning(f"Failed to send photo to admin telegram chat: {exc}")
