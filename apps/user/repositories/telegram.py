from django.utils import timezone

from apps.user.models import TelegramLoginToken


class TelegramRepo:

    @staticmethod
    def create_token(token: str, otp_mode: bool, expires_at) -> TelegramLoginToken:
        return TelegramLoginToken.objects.create(
            token=token,
            status="PENDING",
            otp_mode=otp_mode,
            expires_at=expires_at,
        )

    @staticmethod
    def get_token(token_str: str) -> TelegramLoginToken | None:
        return TelegramLoginToken.objects.filter(token=token_str).first()

    @staticmethod
    def get_pending_token_by_telegram_id(telegram_id: int) -> TelegramLoginToken | None:
        return (
            TelegramLoginToken.objects
            .filter(telegram_id=telegram_id, status="PENDING")
            .order_by("-created_at")
            .first()
        )

    @staticmethod
    def set_telegram_id(row: TelegramLoginToken, telegram_id: int):
        row.telegram_id = telegram_id
        row.save(update_fields=["telegram_id"])

    @staticmethod
    def set_user(row: TelegramLoginToken, user):
        row.user = user
        row.save(update_fields=["user"])

    @staticmethod
    def confirm(row: TelegramLoginToken, user):
        row.user = user
        row.status = "CONFIRMED"
        row.save(update_fields=["user", "status"])

    @staticmethod
    def expire(row: TelegramLoginToken):
        row.status = "EXPIRED"
        row.save(update_fields=["status"])

    @staticmethod
    def confirm_latest_with_user(user):
        row = (
            TelegramLoginToken.objects
            .filter(user=user, status="PENDING")
            .order_by("-created_at")
            .first()
        )
        if row:
            row.status = "CONFIRMED"
            row.save(update_fields=["status"])