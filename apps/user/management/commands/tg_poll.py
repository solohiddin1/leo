import time
import traceback
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.user.services.telegram import TgOtpService


class Command(BaseCommand):
    help = "Poll Telegram for updates (dev alternative to webhook)"

    def handle(self, *args, **kwargs):
        token = settings.TELEGRAM_BOT_TOKEN
        url = f"https://api.telegram.org/bot{token}"
        offset = None

        resp = requests.post(f"{url}/deleteWebhook", json={"drop_pending_updates": True})
        result = resp.json()
        if not result.get("ok"):
            self.stderr.write(f"deleteWebhook failed: {result}")
            return
        self.stdout.write("Polling started...")

        while True:
            try:
                params = {"timeout": 30, "allowed_updates": '["message"]'}
                if offset:
                    params["offset"] = offset
                resp = requests.get(f"{url}/getUpdates", params=params, timeout=35)
                data = resp.json()
                if not data.get("ok"):
                    self.stderr.write(f"getUpdates error: {data}")
                    time.sleep(5)
                    continue
                for update in data.get("result", []):
                    offset = update["update_id"] + 1
                    try:
                        TgOtpService.handle_update(update)
                    except Exception:
                        self.stderr.write(traceback.format_exc())
            except Exception:
                self.stderr.write(traceback.format_exc())
                time.sleep(5)