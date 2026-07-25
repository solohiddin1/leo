from datetime import timezone

from apps.shared.utils.result_codes import ResultCodes
from apps.user.models import User
from apps.shared.utils.utils import success_response, error_response
from apps.user.api.serializers.register import RegisterSerializer
from apps.user.repositories.user_repo import UserRepo

class UserService:
    @staticmethod
    def register(data: dict) -> User:
        user = User.objects.create_user(**data)
        user.save()
        data = RegisterSerializer(user).data
        return success_response(data)

    @staticmethod
    def verify_otp(user_id: int, otp_code: str, ):
        try:
            user = User.objects.get(id=user_id)
            if user is None:
                return error_response(ResultCodes.USER_NOT_FOUND)
            otp = UserRepo.get_user_last_otp(user)
            if otp != otp_code:
                return error_response(ResultCodes.INCORRECT_OTP)
            if otp.is_used:
                return error_response(ResultCodes.OTP_ALREADY_USED)
            if otp.expires_at < timezone.now():
                return error_response(ResultCodes.OTP_EXPIRED)
            return otp
        except Exception:
            return error_response(ResultCodes.UNKNOWN_ERROR)