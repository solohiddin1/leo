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
    INVALID_TOKEN_ERROR = -19
    BONUS_CODE_INVALID = -20
    BONUS_CODE_ALREADY_USED = -21
    BONUS_CODE_NOT_FOUND = -22
    PRODUCT_NOT_FOUND = -23
    CART_ITEM_NOT_FOUND = -24
    CART_EMPTY = -25
    ORDER_NOT_FOUND = -26
    CART_NOT_FOUND = -27
    INSUFFICIENT_BALANCE = -28
    BONUS_CODE_IMAGE_REQUIRED = -29
    INVALID_INPUT = -30
    STORE_NOT_FOUND = -31
    CLAIM_NOT_FOUND = -32
    DEVICE_NOT_FOUND = -33
    NOTIFICATION_NOT_FOUND = -34


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
        "ru": "OTP не найден",
    },
    "PASSWORD_UPDATED_SUCCESS": {
        "uz": "Parol muvaffaqiyatli yangilandi.",
        "en": "Password updated successfully.",
        "ru": "Пароль успешно обновлен.",
    },
    "PASSWORD_UPDATED_FAILURE": {
        "uz": "Login yoki parol noto'g'ri.",
        "en": "Incorrect login or password.",
        "ru": "Неверный логин или пароль.",
    },
    "PROFILE_UPDATED_SUCCESS": {
        "uz": "Profil muvaffaqiyatli yangilandi.",
        "en": "Profile updated successfully.",
        "ru": "Профиль успешно обновлён.",
    },
    "JOB_NOT_FOUND": {
        "uz": "Kasb topilmadi.",
        "en": "Job not found.",
        "ru": "Профессия не найдена.",
    },
    "REGION_NOT_FOUND": {
        "uz": "Hudud topilmadi.",
        "en": "Region not found.",
        "ru": "Регион не найден.",
    },
    "TOO_MANY_REQUESTS": {
        "uz": "Juda ko'p urinish. {wait} soniyadan keyin qayta urinib ko'ring.",
        "en": "Too many attempts. Try again in {wait} sec.",
        "ru": "Слишком много попыток. Повторите попытку через {wait} сек.",
    },
    "INVALID_TOKEN_ERROR": {
        "uz": "Token yaroqsiz yoki muddati tugagan. Qaytadan tizimga kiring.",
        "en": "Invalid or expired token. Please sign in again.",
        "ru": "Токен недействителен или истёк. Войдите в систему заново.",
    },
    "BONUS_CODE_INVALID": {
        "uz": "Bonus kodi noto'g'ri.",
        "en": "Invalid bonus code.",
        "ru": "Неверный бонусный код.",
    },
    "BONUS_CODE_ALREADY_USED": {
        "uz": "Bu bonus kodi allaqachon ishlatilgan.",
        "en": "This bonus code has already been used.",
        "ru": "Этот бонусный код уже был использован.",
    },
    "BONUS_CODE_NOT_FOUND": {
        "uz": "Bonus kodi topilmadi.",
        "en": "Bonus code not found.",
        "ru": "Бонусный код не найден.",
    },
    "PRODUCT_NOT_FOUND": {
        "uz": "Mahsulot topilmadi.",
        "en": "Product not found.",
        "ru": "Товар не найден.",
    },
    "CART_ITEM_NOT_FOUND": {
        "uz": "Savat elementi topilmadi.",
        "en": "Cart item not found.",
        "ru": "Элемент корзины не найден.",
    },
    "CART_EMPTY": {
        "uz": "Savat bo'sh.",
        "en": "Cart is empty.",
        "ru": "Корзина пуста.",
    },
    "ORDER_NOT_FOUND": {
        "uz": "Buyurtma topilmadi.",
        "en": "Order not found.",
        "ru": "Заказ не найден.",
    },
    "CART_NOT_FOUND": {
        "uz": "Savat topilmadi",
        "en": "Cart not found.",
        "ru": "Корзина не найдена.",
    },
    "INSUFFICIENT_BALANCE": {
        "uz": "Hisobingizda mablag' yetarli emas.",
        "en": "Insufficient balance.",
        "ru": "Недостаточно средств на балансе.",
    },
    "BONUS_CODE_IMAGE_REQUIRED": {
        "uz": "Yuklangan rasmlar soni yetarli emas.",
        "en": "Not enough images have been uploaded.",
        "ru": "Загружено недостаточно изображений.",
    },
    "INVALID_INPUT": {
        "uz": "Noto'g'ri ma'lumot kiritildi.",
        "en": "Invalid input.",
        "ru": "Неверный ввод.",
    },
    "STORE_NOT_FOUND": {
        "uz": "Do'kon topilmadi.",
        "en": "Store not found.",
        "ru": "Магазин не найден.",
    },
    "CLAIM_NOT_FOUND": {
        "uz": "Ariza topilmadi.",
        "en": "Claim not found.",
        "ru": "Заявка не найдена.",
    },
    "DEVICE_NOT_FOUND": {
        "uz": "Qurilma topilmadi.",
        "en": "Device not found.",
        "ru": "Устройство не найдено.",
    },
    "NOTIFICATION_NOT_FOUND": {
        "uz": "Bildirishnoma topilmadi.",
        "en": "Notification not found.",
        "ru": "Уведомление не найдено.",
    },
}
