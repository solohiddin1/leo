from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from apps.shared.utils.result_codes import ResultCodes
from apps.user.models import User
from apps.shared.utils.utils import success_response, error_response
from apps.user.repositories.user_repo import UserRepo
from apps.user.services.sms import SmsService
from apps.order.repositories.cart_repo import CartRepo

class UserService:
    @staticmethod
    def register(data: dict) -> User:
        device_id = data.pop("device_id")
        user = UserRepo.get_user_by_username(data["username"])
        if user is None:
            user = User.objects.create_user(**data)
        user.save()
        CartRepo.get_or_create_cart(user)
        otp = SmsService.generate_otp()

        return success_response(
            {
                "username": user.username,
                "otp": otp
            }
        )

    @staticmethod
    def login(username: str, password: str):
        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return error_response(ResultCodes.INVALID_CREDENTIALS)
        return success_response(
            UserService.token_for_user(user)
        )

    @staticmethod
    def set_user_password(user: User, password: str):
        user.set_password(password)
        user.save()
        return success_response(ResultCodes.PASSWORD_UPDATED_SUCCESS)

    @staticmethod
    def verify_otp(user_id: int, otp_code: str, ):
        try:
            user = UserRepo.get_user_by_id(user_id)
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
            otp.is_used = True
            otp.is_verified = True
            otp.save(update_fields=["is_used", "is_verified"])
            return otp
        except Exception:
            return error_response(ResultCodes.UNKNOWN_ERROR)

    @staticmethod
    def token_for_user(user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }