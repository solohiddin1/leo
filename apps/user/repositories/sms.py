from django.utils import timezone
from datetime import timedelta

from apps.user.models import Otp


class SmsRepo:
    @staticmethod
    def create_otp(user, otp_code, expires_in_seconds) -> Otp:
        return Otp.objects.create(
            user=user,
            code=otp_code,
            phone_number=user.username or "",
            expires_at=timezone.now() + timedelta(seconds=expires_in_seconds),
        )

    @staticmethod
    def get_otp_of_user(user):
        return Otp.objects.filter(user=user)

    @staticmethod
    def get_valid_otp(user_id: int, code: str) -> Otp | None:
        return Otp.objects.filter(
            user_id=user_id,
            code=code,
            is_used=False,
            expires_at__gt=timezone.now(),
        ).last()
