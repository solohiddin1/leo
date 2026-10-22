from apps.transaction.services.bonus_service import BonusService
from apps.user.models import User
from apps.user.repositories.user_repo import UserRepo


def resolve_telegram_user(
    telegram_chat_id: int,
    phone: str = "",
    first_name: str = "",
    telegram_username: str = "",
    lang: str = "uz",
    region_id: int = None,
) -> User:
    """Same get-or-create convention as apps/user/services/telegram.py:
    _link_or_create_user, but for a Telegram identity coming from usta-source's bot
    instead of leo's own login bot. Verified immediately: usta-source already collects
    the phone number at bot registration (no separate OTP step there)."""
    telegram_id = str(telegram_chat_id)

    user = UserRepo.get_user_by_telegram_id(telegram_id)
    if user:
        return user

    if phone:
        user = UserRepo.get_user_by_username(phone)

    is_new = False
    if not user:
        user = UserRepo.create_telegram_user(
            username=phone or f"tg_{telegram_id}",
            first_name=first_name,
            last_name="",
        )
        is_new = True
        if lang in ("uz", "ru"):
            user.lang = lang
        if region_id:
            user.region_id = region_id

    UserRepo.attach_telegram(user, telegram_id, telegram_username)
    if not user.is_verified:
        user.is_verified = True
        user.save(update_fields=["is_verified", "lang", "region_id"] if is_new else ["is_verified"])
    elif is_new:
        user.save(update_fields=["lang", "region_id"])

    if is_new:
        BonusService.award_signup_bonus(user)

    return user
