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
        from apps.order.repositories.cart_repo import CartRepo
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone_number if phone_number else None
            }
        )
        CartRepo.get_or_create_cart(user)
        return user

    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        return User.objects.filter(id=user_id).first()

    @staticmethod
    def update_profile(user: User, region_id: int | None, job_id: int | None) -> User:
        if region_id is not None:
            user.region_id = region_id
        if job_id is not None:
            user.job_id = job_id
        user.save(update_fields=["region_id", "job_id"])
        return user