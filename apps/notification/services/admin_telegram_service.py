import json as json_lib
from concurrent.futures import ThreadPoolExecutor

import requests
from django.conf import settings

from apps.shared.middleware.middleware import get_logger

logger = get_logger()
executor = ThreadPoolExecutor(max_workers=2)


class AdminTelegramNotifier:

    @classmethod
    def get_token(cls) -> str:
        return settings.TELEGRAM_ADMIN_BOT_TOKEN or settings.TELEGRAM_BOT_TOKEN or ""

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
    def send(cls, text: str, reply_markup: dict = None) -> None:
        token = cls.get_token()
        if not token or not settings.TELEGRAM_ADMIN_CHAT_ID:
            return
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {
                "chat_id": settings.TELEGRAM_ADMIN_CHAT_ID,
                "text": text,
                "parse_mode": "HTML",
            }
            if reply_markup is not None:
                payload["reply_markup"] = reply_markup
            executor.submit(cls.send_heavy_request, url, data=payload)
            logger.info(f"Notified admin telegram chat: {text}")
        except Exception as exc:
            logger.warning(f"Failed to notify admin telegram chat: {exc}")

    @classmethod
    def send_photo(cls, photo_file, caption: str = "", reply_markup: dict = None) -> None:
        token = cls.get_token()
        if not token or not settings.TELEGRAM_ADMIN_CHAT_ID:
            return
        try:
            url = f"https://api.telegram.org/bot{token}/sendPhoto"
            data = {
                "chat_id": settings.TELEGRAM_ADMIN_CHAT_ID,
                "caption": caption,
                "parse_mode": "HTML",
            }
            if reply_markup is not None:
                data["reply_markup"] = json_lib.dumps(reply_markup)

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

    @classmethod
    def answer_callback_query(cls, callback_query_id: str, text: str = None, show_alert: bool = False):
        token = cls.get_token()
        if not token or not callback_query_id:
            return
        try:
            url = f"https://api.telegram.org/bot{token}/answerCallbackQuery"
            payload = {"callback_query_id": callback_query_id}
            if text:
                payload["text"] = text
                payload["show_alert"] = show_alert
            executor.submit(cls.send_heavy_request, url, data=payload)
        except Exception as exc:
            logger.warning(f"Failed to answer callback query: {exc}")

    @classmethod
    def edit_message_text(cls, chat_id, message_id, text: str, reply_markup: dict = None):
        token = cls.get_token()
        if not token or not chat_id or not message_id:
            return
        try:
            url = f"https://api.telegram.org/bot{token}/editMessageText"
            payload = {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": text,
                "parse_mode": "HTML",
            }
            if reply_markup is not None:
                payload["reply_markup"] = reply_markup
            executor.submit(cls.send_heavy_request, url, data=payload)
        except Exception as exc:
            logger.warning(f"Failed to edit message text: {exc}")

    @classmethod
    def edit_message_caption(cls, chat_id, message_id, caption: str, reply_markup: dict = None):
        token = cls.get_token()
        if not token or not chat_id or not message_id:
            return
        try:
            url = f"https://api.telegram.org/bot{token}/editMessageCaption"
            payload = {
                "chat_id": chat_id,
                "message_id": message_id,
                "caption": caption,
                "parse_mode": "HTML",
            }
            if reply_markup is not None:
                payload["reply_markup"] = reply_markup
            executor.submit(cls.send_heavy_request, url, data=payload)
        except Exception as exc:
            logger.warning(f"Failed to edit message caption: {exc}")

    @classmethod
    def edit_message_reply_markup(cls, chat_id, message_id, reply_markup: dict = None):
        token = cls.get_token()
        if not token or not chat_id or not message_id:
            return
        try:
            url = f"https://api.telegram.org/bot{token}/editMessageReplyMarkup"
            payload = {
                "chat_id": chat_id,
                "message_id": message_id,
            }
            if reply_markup is not None:
                payload["reply_markup"] = reply_markup
            executor.submit(cls.send_heavy_request, url, data=payload)
        except Exception as exc:
            logger.warning(f"Failed to edit message reply markup: {exc}")
