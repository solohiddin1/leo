from apps.user.models import User, Otp

class UserRepo:

    @staticmethod
    def get_user_by_username(username: str) -> User | None:
        return User.objects.filter(username=username).first()

    @staticmethod
    def get_user_last_otp(user: User) -> Otp | None:
        return Otp.objects.filter(user=user).last()

    @staticmethod
    def get_user_by_telegram_id(telegram_id: int) -> User | None:
        return User.objects.filter(telegram_id=telegram_id).first()

    @classmethod
    def attach_telegram(cls, user, telegram_id, telegram_username):
        user.telegram_id = telegram_id
        user.telegram_username = telegram_username
        user.save(update_fields=["telegram_id", "telegram_username"])
        return user

    @classmethod
    def create_telegram_user(cls, username: str, first_name: str, last_name:str, phone_number:str) -> User | None:
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        return user

    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        return User.objects.filter(id=user_id).first()