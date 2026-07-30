from django.utils import timezone

from apps.shared.utils.result_codes import ResultCodes
from apps.user.models import User
from apps.shared.utils.utils import success_response, error_response
from apps.user.repositories.user_repo import UserRepo
from apps.user.services.sms import SmsService

class UserService:
    @staticmethod
    def register(data: dict) -> User:
        device_id = data.pop("device_id")
        user = UserRepo.get_user_by_username(data["username"])
        if user is None:
            user = User.objects.create_user(**data)
        user.save()
        otp = SmsService.generate_otp()

        return success_response(
            {
                "username": user.username,
                "otp": otp
            }
        )

    @staticmethod
    def verify_otp(user_id: int, otp_code: str, ):
        try:
            user = User.objects.get(id=user_id)
            if user is None:
                return error_response(ResultCodes.USER_NOT_FOUND)
            otp = UserRepo.get_user_last_otp(user)
            if otp is None:
                return error_response(ResultCodes.OTP_EXPIRED)
            if otp != otp_code:
                return error_response(ResultCodes.INCORRECT_OTP)
            if otp.is_used:
                return error_response(ResultCodes.OTP_ALREADY_USED)
            if otp.expires_at < timezone.now():
                return error_response(ResultCodes.OTP_EXPIRED)
            return otp
        except Exception:
            return error_response(ResultCodes.UNKNOWN_ERROR)