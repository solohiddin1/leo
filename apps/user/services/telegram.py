import secrets
import requests
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from apps.shared.models import SiteConfig
from apps.user.repositories.sms import SmsRepo
from apps.user.repositories.telegram import TelegramRepo
from apps.user.repositories.user_repo import UserRepo
from apps.user.services.sms import SmsService

SUCCESS_MSG = "✅ Muvaffaqiyatli kirdingiz! Saytga qaytishingiz mumkin."
SUCCESS_MSG_WITH_URL = "✅ Muvaffaqiyatli kirdingiz!\n\n👉 Saytga qaytish: {url}"
NO_TOKEN_MSG = "Kirish uchun saytdagi «Telegram orqali kirish» tugmasini bosing."
NO_TOKEN_MSG_WITH_URL = "Kirish uchun saytdagi «Telegram orqali kirish» tugmasini bosing:\n\n👉 {url}"
EXPIRED_MSG = "⚠️ Havola eskirgan yoki yaroqsiz. Iltimos, saytdan qayta urinib ko'ring."
ASK_PHONE_MSG = "Kirishni yakunlash uchun telefon raqamingizni ulashing 👇"
WRONG_CONTACT_MSG = "Iltimos, o'zingizning telefon raqamingizni ulashing."
OTP_TIME_LIMIT_MSG = "Iltimos otp so'rovi uchun {seconds} sekund kuting"

CONTACT_KEYBOARD = {
    "keyboard": [[{"text": "📱 Telefon raqamni ulashish", "request_contact": True}]],
    "resize_keyboard": True,
    "one_time_keyboard": True,
}
REMOVE_KEYBOARD = {"remove_keyboard": True}


class TelegramClient:
    @classmethod
    def send_message(cls, chat_id, text, reply_markup=None):
        if not settings.TELEGRAM_BOT_TOKEN:
            return
        payload = {"chat_id": chat_id, "text": text}
        if reply_markup is not None:
            payload["reply_markup"] = reply_markup
        try:
            requests.post(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                json=payload,
                timeout=10,
            )
        except Exception as e:
            print(e)


class TgOtpService:
    @classmethod
    def request(cls):
        config = SiteConfig.objects.first()
        otp_mode = config.send_otp_code if config else False

        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(minutes=settings.TELEGRAM_LOGIN_TOKEN_TTL_MINUTES)
        TelegramRepo.create_token(token, otp_mode, expires_at)
        return {
            "token": token,
            "deep_link": f"https://t.me/{settings.TELEGRAM_BOT_USERNAME}?start={token}",
            "poll": not otp_mode,
        }

    @classmethod
    def _handle_start(cls, chat_id, telegram_id, frm, text):
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            TelegramClient.send_message(chat_id, cls._no_token_msg(), reply_markup=REMOVE_KEYBOARD)
            return
        token_str = parts[1].strip()

        row = TelegramRepo.get_token(token_str)
        if not row:
            return
        if not cls._is_usable(row):
            TelegramClient.send_message(chat_id, EXPIRED_MSG)
            return

        TelegramRepo.set_telegram_id(row, telegram_id)

        if row.otp_mode:
            user = UserRepo.get_user_by_telegram_id(telegram_id) or cls._link_or_create_user("", telegram_id, frm)
            TelegramRepo.set_user(row, user)
            sent, result = SmsService.create_otp_for_user(user)
            if sent:
                TelegramClient.send_message(chat_id, cls._otp_msg(result))
            else:
                TelegramClient.send_message(chat_id, OTP_TIME_LIMIT_MSG.format(seconds=result))
            return

        user = UserRepo.get_user_by_telegram_id(telegram_id)
        if user:
            TelegramRepo.confirm(row, user)
            TelegramClient.send_message(chat_id, cls._success_msg(), reply_markup=REMOVE_KEYBOARD)
        else:
            TelegramClient.send_message(chat_id, ASK_PHONE_MSG, reply_markup=CONTACT_KEYBOARD)

    @classmethod
    def poll(cls, token_str):
        row = TelegramRepo.get_token(token_str)
        if not row:
            return {"error": "invalid"}

        if row.status == "CONFIRMED" and row.user_id:
            user = row.user
            if user is None:
                return {"error": "invalid"}
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            TelegramRepo.expire(row)
            return {
                "status": "CONFIRMED",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }

        if row.status == "EXPIRED" or timezone.now() > row.expires_at:
            if row.status == "PENDING":
                TelegramRepo.expire(row)
            return {"error": "expired"}

        return {"status": "PENDING"}

    @classmethod
    def verify_otp(cls, token_str, code):
        row = TelegramRepo.get_token(token_str)
        if not cls._is_usable(row):
            return {"error": "expired"}
        if not row.otp_mode or not row.user_id:
            return {"error": "invalid"}

        otp = SmsRepo.get_valid_otp(row.user_id, str(code))
        if not otp:
            return {"error": "invalid_otp"}

        otp.is_used = True
        otp.is_verified = True
        otp.save(update_fields=["is_used", "is_verified"])
        TelegramRepo.confirm(row, row.user)

        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(row.user)
        return {
            "status": "CONFIRMED",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    @classmethod
    def _handle_contact(cls, chat_id, telegram_id, frm, contact):
        if contact.get("user_id") != telegram_id:
            TelegramClient.send_message(chat_id, WRONG_CONTACT_MSG)
            return

        row = TelegramRepo.get_pending_token_by_telegram_id(telegram_id)
        if not row:
            return
        if not cls._is_usable(row):
            TelegramClient.send_message(chat_id, EXPIRED_MSG, reply_markup=REMOVE_KEYBOARD)
            return

        phone = cls._normalize_phone(contact.get("phone_number") or "")
        user = cls._link_or_create_user(phone, telegram_id, frm)

        config = SiteConfig.objects.first()
        if config and config.send_otp_code:
            sent, result = SmsService.create_otp_for_user(user)
            if not sent:
                TelegramClient.send_message(chat_id, OTP_TIME_LIMIT_MSG.format(seconds=result))
                return
            TelegramRepo.confirm(row, user)
            TelegramClient.send_message(chat_id, cls._otp_msg(result))
        else:
            user.is_verified = True
            user.save(update_fields=["is_verified"])
            TelegramRepo.confirm(row, user)
            TelegramClient.send_message(chat_id, cls._success_msg(), reply_markup=REMOVE_KEYBOARD)

    @classmethod
    def handle_update(cls, update):
        message = update.get("message") or {}
        frm = message.get("from") or {}
        telegram_id = frm.get("id")
        if not telegram_id:
            return

        chat_id = (message.get("chat") or {}).get("id") or telegram_id
        contact = message.get("contact")

        if contact:
            cls._handle_contact(chat_id, telegram_id, frm, contact)
            return

        text = message.get("text") or ""
        if text.startswith("/start"):
            cls._handle_start(chat_id, telegram_id, frm, text)

    @staticmethod
    def _success_msg():
        url = settings.TELEGRAM_LOGIN_RETURN_URL
        return SUCCESS_MSG_WITH_URL.format(url=url) if url else SUCCESS_MSG

    @staticmethod
    def _otp_msg(otp):
        return f"Ilovaga kirish uchun OTP kodingiz: {otp}"

    @staticmethod
    def _no_token_msg():
        url = settings.TELEGRAM_LOGIN_RETURN_URL
        return NO_TOKEN_MSG_WITH_URL.format(url=url) if url else NO_TOKEN_MSG

    @staticmethod
    def _is_usable(row):
        return bool(row) and row.status == "PENDING" and timezone.now() <= row.expires_at

    @staticmethod
    def _normalize_phone(raw):
        digits = "".join(ch for ch in raw if ch.isdigit())
        if len(digits) == 9:
            digits = "998" + digits
        return digits

    @classmethod
    def _link_or_create_user(cls, phone, telegram_id, frm):
        user = UserRepo.get_user_by_username(phone) if phone else None
        if not user:
            user = UserRepo.create_telegram_user(
                username=phone or f"tg_{telegram_id}",
                first_name=frm.get("first_name") or "",
                last_name=frm.get("last_name") or "",
                phone_number=phone or "",
            )
        UserRepo.attach_telegram(user, telegram_id, frm.get("username"))
        return user