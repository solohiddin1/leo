from apps.user.models import User, Otp

class UserRepo:

    @staticmethod
    def get_user_last_otp(user: User) -> Otp | None:
        return Otp.objects.filter(user=user).last()