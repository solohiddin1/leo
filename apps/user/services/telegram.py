import secrets
from datetime import timedelta

import requests
from django.conf import settings
from django.utils import timezone

from apps.shared.middleware.middleware import get_logger
from apps.shared.models import SiteConfig
from apps.shared.utils.result_codes import ResultCodes
from apps.user.repositories.sms import SmsRepo
from apps.user.repositories.telegram import TelegramRepo
from apps.user.repositories.user_repo import UserRepo
from apps.user.services.sms import SmsService

logger = get_logger()

SUCCESS_MSG = "✅ Muvaffaqiyatli kirdingiz! Ilovaga qaytishingiz mumkin."
SUCCESS_MSG_WITH_URL = "✅ Muvaffaqiyatli kirdingiz!\n\n👉 Ilovaga qaytish: {url}"
NO_TOKEN_MSG = "Kirish uchun ilovadagi «Telegram orqali kirish» tugmasini bosing."
NO_TOKEN_MSG_WITH_URL = (
    "Kirish uchun ilovadagi «Telegram orqali kirish» tugmasini bosing:\n\n👉 {url}"
)
EXPIRED_MSG = "⚠️ Havola eskirgan yoki yaroqsiz. Iltimos, ilovadan qayta urinib ko'ring."
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
        expires_at = timezone.now() + timedelta(
            minutes=settings.TELEGRAM_LOGIN_TOKEN_TTL_MINUTES
        )
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
            TelegramClient.send_message(
                chat_id, cls._no_token_msg(), reply_markup=REMOVE_KEYBOARD
            )
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
            user = UserRepo.get_user_by_telegram_id(telegram_id)
            if not user:
                TelegramRepo.set_telegram_id(row, telegram_id)
                TelegramClient.send_message(
                    chat_id, ASK_PHONE_MSG, reply_markup=CONTACT_KEYBOARD
                )
                return
            TelegramRepo.set_user(row, user)
            sent, result = SmsService.create_otp_for_user(user)
            if sent:
                TelegramClient.send_message(chat_id, cls._otp_msg(result))
            else:
                TelegramClient.send_message(
                    chat_id, OTP_TIME_LIMIT_MSG.format(seconds=result)
                )
            return

        user = UserRepo.get_user_by_telegram_id(telegram_id)
        if user:
            if not user.is_verified:
                user.is_verified = True
                user.save(update_fields=["is_verified"])
            TelegramRepo.confirm(row, user)
            TelegramClient.send_message(
                chat_id, cls._success_msg(), reply_markup=REMOVE_KEYBOARD
            )
        else:
            TelegramClient.send_message(
                chat_id, ASK_PHONE_MSG, reply_markup=CONTACT_KEYBOARD
            )

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

        user = row.user
        if not user.is_verified:
            user.is_verified = True
            user.save(update_fields=["is_verified"])

        TelegramRepo.confirm(row, user)

        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(row.user)
        return {
            "status": "CONFIRMED",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    @classmethod
    def _handle_contact(cls, chat_id, telegram_id, frm, contact):
        logger.info(f"contact : {contact}, {contact.get('phone_number')} phone number")
        if contact.get("user_id") != telegram_id:
            TelegramClient.send_message(chat_id, WRONG_CONTACT_MSG)
            return

        row = TelegramRepo.get_pending_token_by_telegram_id(telegram_id)
        logger.info(f"contact from telegram login {row}, {telegram_id}")
        if not row:
            return
        if not cls._is_usable(row):
            TelegramClient.send_message(
                chat_id, EXPIRED_MSG, reply_markup=REMOVE_KEYBOARD
            )
            return

        phone = cls._normalize_phone(contact.get("phone_number") or "")
        user = cls._link_or_create_user(phone, telegram_id, frm)

        if row.otp_mode:
            sent, result = SmsService.create_otp_for_user(user)
            if not sent:
                TelegramClient.send_message(
                    chat_id, OTP_TIME_LIMIT_MSG.format(seconds=result)
                )
                return
            TelegramRepo.set_user(row, user)
            TelegramClient.send_message(chat_id, cls._otp_msg(result))
        else:
            user.is_verified = True
            user.save(update_fields=["is_verified"])
            TelegramRepo.confirm(row, user)
            TelegramClient.send_message(
                chat_id, cls._success_msg(), reply_markup=REMOVE_KEYBOARD
            )

    @classmethod
    def handle_update(cls, update):
        if "callback_query" in update:
            cls._handle_callback_query(update["callback_query"])
            logger.info(update["callback_query"])
            return

        message = update.get("message") or {}
        if message.get("reply_to_message"):
            cls._handle_reply_message(message)
            return

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

    @classmethod
    def _handle_callback_query(cls, cb):
        from apps.notification.services.admin_telegram_service import AdminTelegramNotifier
        from apps.order.models import Order, OrderState
        from apps.order.repositories.order_repo import OrderRepo
        from apps.transaction.models import BonusClaimStatus, UserSumma
        from apps.transaction.services.bonus_service import BonusService

        cb_id = cb.get("id")
        data = cb.get("data") or ""
        message = cb.get("message") or {}
        chat_id = (message.get("chat") or {}).get("id")
        msg_id = message.get("message_id")
        from_user = cb.get("from") or {}
        admin_username = from_user.get("username") or from_user.get("first_name") or "Admin"

        if data.startswith("approve_order_"):
            try:
                order_id = int(data.replace("approve_order_", ""))
                order = Order.objects.filter(id=order_id).first()
                if not order:
                    AdminTelegramNotifier.answer_callback_query(cb_id, text="Buyurtma topilmadi", show_alert=True)
                    return
                if order.state != OrderState.PENDING:
                    AdminTelegramNotifier.answer_callback_query(cb_id, text=f"Buyurtma allaqachon {order.state} holatida", show_alert=True)
                    return
                OrderRepo.approve_order(order)
                AdminTelegramNotifier.answer_callback_query(cb_id, text="✅ Buyurtma tasdiqlandi!")
                if chat_id and msg_id:
                    new_text = (message.get("text") or message.get("caption") or f"Order #{order_id}") + f"\n\n✅ <b>Tasdiqlandi (@{admin_username})</b>"
                    if message.get("caption"):
                        AdminTelegramNotifier.edit_message_caption(chat_id, msg_id, new_text)
                    else:
                        AdminTelegramNotifier.edit_message_text(chat_id, msg_id, new_text)
            except Exception as e:
                logger.warning(f"Error in approve_order callback: {e}")

        elif data.startswith("reject_order_"):
            try:
                order_id = int(data.replace("reject_order_", ""))
                order = Order.objects.filter(id=order_id).first()
                if not order:
                    AdminTelegramNotifier.answer_callback_query(cb_id, text="Buyurtma topilmadi", show_alert=True)
                    return
                if order.state != OrderState.PENDING:
                    AdminTelegramNotifier.answer_callback_query(cb_id, text=f"Buyurtma allaqachon {order.state} holatida", show_alert=True)
                    return
                AdminTelegramNotifier.answer_callback_query(cb_id, text="Iltimos, bekor qilish sababini kiriting")
                prompt_text = f"❌ Buyurtma #{order_id} bekor qilish sababini ushbu xabarga reply tarzida yozing:"
                force_reply = {"force_reply": True, "selective": True}
                AdminTelegramNotifier.send(prompt_text, reply_markup=force_reply)
            except Exception as e:
                logger.warning(f"Error in reject_order callback: {e}")

        elif data.startswith("approve_bonus_"):
            try:
                claim_id = int(data.replace("approve_bonus_", ""))
                claim = UserSumma.objects.filter(id=claim_id).first()
                if not claim:
                    AdminTelegramNotifier.answer_callback_query(cb_id, text="Ariza topilmadi", show_alert=True)
                    return
                if claim.status != BonusClaimStatus.PENDING:
                    AdminTelegramNotifier.answer_callback_query(cb_id, text=f"Ariza allaqachon {claim.status} holatida", show_alert=True)
                    return
                BonusService.approve_claim(claim_id, admin_user=None)
                AdminTelegramNotifier.answer_callback_query(cb_id, text="✅ Bonus ariza tasdiqlandi!")
                if chat_id and msg_id:
                    new_text = (message.get("text") or message.get("caption") or f"Claim #{claim_id}") + f"\n\n✅ <b>Tasdiqlandi (@{admin_username})</b>"
                    if message.get("caption"):
                        AdminTelegramNotifier.edit_message_caption(chat_id, msg_id, new_text)
                    else:
                        AdminTelegramNotifier.edit_message_text(chat_id, msg_id, new_text)
            except Exception as e:
                logger.warning(f"Error in approve_bonus callback: {e}")

        elif data.startswith("reject_bonus_"):
            try:
                claim_id = int(data.replace("reject_bonus_", ""))
                claim = UserSumma.objects.filter(id=claim_id).first()
                if not claim:
                    AdminTelegramNotifier.answer_callback_query(cb_id, text="Ariza topilmadi", show_alert=True)
                    return
                if claim.status != BonusClaimStatus.PENDING:
                    AdminTelegramNotifier.answer_callback_query(cb_id, text=f"Ariza allaqachon {claim.status} holatida", show_alert=True)
                    return
                AdminTelegramNotifier.answer_callback_query(cb_id, text="Iltimos, bekor qilish sababini kiriting")
                prompt_text = f"❌ Bonus ariza #{claim_id} bekor qilish sababini ushbu xabarga reply tarzida yozing:"
                force_reply = {"force_reply": True, "selective": True}
                AdminTelegramNotifier.send(prompt_text, reply_markup=force_reply)
            except Exception as e:
                logger.warning(f"Error in reject_bonus callback: {e}")

    @classmethod
    def _handle_reply_message(cls, message):
        import re

        from apps.notification.services.admin_telegram_service import AdminTelegramNotifier
        from apps.order.models import Order
        from apps.order.repositories.order_repo import OrderRepo
        from apps.transaction.services.bonus_service import BonusService

        reply_to = message.get("reply_to_message") or {}
        parent_text = reply_to.get("text") or reply_to.get("caption") or ""
        reason = (message.get("text") or "").strip()

        order_match = re.search(r"Buyurtma\s+#(\d+)\s+bekor\s+qilish", parent_text)
        if order_match:
            order_id = int(order_match.group(1))
            order = Order.objects.filter(id=order_id).first()
            if order:
                OrderRepo.reject_order(order)
                AdminTelegramNotifier.send(f"❌ Buyurtma #{order_id} bekor qilindi.\n<b>Sabab:</b> {reason}")
            return

        bonus_match = re.search(r"Bonus\s+ariza\s+#(\d+)\s+bekor\s+qilish", parent_text)
        if bonus_match:
            claim_id = int(bonus_match.group(1))
            BonusService.reject_claim(claim_id, admin_user=None, reason=reason)
            AdminTelegramNotifier.send(f"❌ Bonus ariza #{claim_id} bekor qilindi.\n<b>Sabab:</b> {reason}")
            return

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
        return (
            bool(row) and row.status == "PENDING" and timezone.now() <= row.expires_at
        )

    @staticmethod
    def _normalize_phone(raw):
        digits = "".join(ch for ch in raw if ch.isdigit())
        if len(digits) == 9:
            digits = "998" + digits
        return digits

    @classmethod
    def _link_or_create_user(cls, phone, telegram_id, frm):
        user = None
        if phone:
            user = UserRepo.get_user_by_username(phone)
        logger.info(
            f"phone for creating telegram user {phone}, {telegram_id}, frm "
            f"{frm.get('first_name')}, {frm.get('last_name')}"
        )
        if not user:
            user = UserRepo.create_telegram_user(
                username=phone or f"tg_{telegram_id}",
                first_name=frm.get("first_name") or "",
                last_name=frm.get("last_name") or "",
            )
        UserRepo.attach_telegram(user, telegram_id, frm.get("username"))
        return user
