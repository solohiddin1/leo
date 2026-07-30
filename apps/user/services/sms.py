import random
from datetime import timedelta

from django.utils import timezone

from apps.shared.models import SiteConfig
from apps.user.models import Otp
from apps.user.repositories.sms import SmsRepo

class SmsService:

    @staticmethod
    def send_sms(request):
        pass

    @staticmethod
    def generate_otp() -> int:
        otp = random.randint(1000, 9999)
        return otp

    @staticmethod
    def check_otp(request):
        pass

    @staticmethod
    def create_otp_for_user(user) -> tuple[bool, int]:
        allowed, seconds = SmsService.check_otp_generation(user)
        if not allowed:
            return False, seconds
        code = SmsService.generate_otp()
        otp = SmsRepo.create_otp(user, code, 300)
        return True, int(otp.code)

    @staticmethod
    def check_otp_generation(user) -> tuple[bool, int]:
        if user.is_developer:
            return True, 0
        otp = Otp.objects.filter(user=user).last()
        if not otp:
            return True, 0

        config = SiteConfig.objects.first()
        cooldown_seconds = config.otp_wait_seconds if config else 60
        cooldown = timedelta(seconds=cooldown_seconds)

        elapsed = timezone.now() - otp.created_at
        if elapsed > cooldown:
            return True, 0
        remaining = cooldown - elapsed
        return False, int(remaining.total_seconds())
