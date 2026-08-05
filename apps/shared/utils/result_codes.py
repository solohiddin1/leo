from enum import Enum

class ResultCodes(Enum):
    SUCCESS = 0
    UNKNOWN_ERROR = -1
    USER_ALREADY_REGISTERED = -2
    USER_NOT_FOUND = -3
    WRONG_VERIFICATION_CODE = -4
    INVALID_CREDENTIALS = -5
    INVALID_REFRESH_TOKEN = -6
    PRODUCT_QUANTITY_NOT_ENOUGH = -7
    INCORRECT_OTP = -8
    BANNER_NOT_FOUND = -9
    OTP_EXPIRED = -10
    OTP_ALREADY_USED = -11
    OTP_NOT_FOUND = -12
    PASSWORD_UPDATED_SUCCESS = -13
    PASSWORD_UPDATED_FAILURE = -14
    PROFILE_UPDATED_SUCCESS = -15
    JOB_NOT_FOUND = -16
    REGION_NOT_FOUND = -17
    TOO_MANY_REQUESTS = -18

ResultMessages = {
    "SUCCESS": {
        "uz": "Muvaffaqiyatli.",
        "en": "Success.",
        "ru": "Успешно.",
    },
    "UNKNOWN_ERROR": {
        "uz": "Noma'lum xato.",
        "en": "Unknown error.",
        "ru": "Неизвестная ошибка.",
    },
    "USER_ALREADY_REGISTERED": {
        "uz": "Foydalanuvchi allaqachon ro'yxatdan o'tgan.",
        "en": "User already registered.",
        "ru": "Пользователь уже зарегистрирован.",
    },
    "USER_NOT_FOUND": {
        "uz": "Foydalanuvchi topilmadi.",
        "en": "User not found.",
        "ru": "Пользователь не найден.",
    },
    "WRONG_VERIFICATION_CODE": {
        "uz": "Tasdiqlash kodi noto'g'ri.",
        "en": "Wrong verification code.",
        "ru": "Неверный код подтверждения.",
    },
    "INVALID_CREDENTIALS": {
        "uz": "Login yoki parol noto'g'ri.",
        "en": "Invalid credentials.",
        "ru": "Неверные учётные данные.",
    },
    "INVALID_REFRESH_TOKEN": {
        "uz": "Yangilash tokeni yaroqsiz.",
        "en": "Invalid refresh token.",
        "ru": "Недействительный токен обновления.",
    },
    "PRODUCT_QUANTITY_NOT_ENOUGH": {
        "uz": "Mahsulot miqdori yetarli emas.",
        "en": "Product quantity not enough.",
        "ru": "Недостаточное количество товара.",
    },
    "INCORRECT_OTP": {
        "uz": "Kiritilgan kod noto'g'ri.",
        "en": "Incorrect OTP.",
        "ru": "Неверный OTP.",
    },
    "BANNER_NOT_FOUND": {
        "uz": "Banner topilmadi.",
        "en": "Banner not found.",
        "ru": "Баннер не найден.",
    },
    "OTP_EXPIRED": {
        "uz": "Kiritilgan kod muddati o'tgan.",
        "en": "OTP expired.",
        "ru": "Срок действия OTP истёк.",
    },
    "OTP_ALREADY_USED": {
        "uz": "Kiritilgan kod allaqachon ishlatilgan.",
        "en": "OTP already used.",
        "ru": "OTP уже использован.",
    },
    "OTP_NOT_FOUND": {
        "uz": "Kiritilgan kod topilmadi",
        "en": "OTP not found.",
        "ru": "OTP не найден"
    },
    "PASSWORD_UPDATED_SUCCESS": {
        "uz": "Parol muvaffaqiyatli yangilandi.",
        "en": "Password updated successfully.",
        "ru": "Пароль успешно обновлен."
    },
    "PASSWORD_UPDATED_FAILURE": {
        "uz": "Login yoki parol noto'g'ri.",
        "en": "Incorrect login or password.",
        "ru": "Неверный логин или пароль."
    },
    "PROFILE_UPDATED_SUCCESS": {
        "uz": "Profil muvaffaqiyatli yangilandi.",
        "en": "Profile updated successfully.",
        "ru": "Профиль успешно обновлён."
    },
    "JOB_NOT_FOUND": {
        "uz": "Kasb topilmadi.",
        "en": "Job not found.",
        "ru": "Профессия не найдена."
    },
    "REGION_NOT_FOUND": {
        "uz": "Hudud topilmadi.",
        "en": "Region not found.",
        "ru": "Регион не найден."
    },
    "TOO_MANY_REQUESTS": {
        "uz": "Juda ko'p urinish. {wait} soniyadan keyin qayta urinib ko'ring.",
        "en": "Too many attempts. Try again in {wait} sec.",
        "ru": "Слишком много попыток. Повторите попытку через {wait} сек.",
    },
}