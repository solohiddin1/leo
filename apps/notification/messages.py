from dataclasses import dataclass
from enum import IntEnum


class NotificationType(IntEnum):
    ORDER_CREATED = 1
    ORDER_CANCELED_BY_CLIENT = 2
    BONUS_CODE_REGISTERED = 3
    CHALLENGE_COMPLETED = 4
    ORDER_ACCEPTED = 5
    ORDER_REJECTED = 6
    ORDER_COMPLETED = 7
    BONUS_CLAIM_APPROVED = 8
    BONUS_CLAIM_REJECTED = 9
    SIGNUP_BONUS = 10
    POINTS_EXPIRING_WARNING = 11
    POINTS_EXPIRED = 12


@dataclass(frozen=True)
class NotificationMessage:
    title: dict[str, str]
    body: dict[str, str]
    image: dict[str, str | None]
    type: NotificationType

    def render(self, lang: str | None, **kwargs) -> tuple[str, str]:
        lang_key = (lang or "UZ").upper()
        if lang_key not in self.title and len(lang_key) > 2:
            lang_key = lang_key[:2]
        title = self.title.get(lang_key, self.title.get("UZ", ""))
        body = self.body.get(lang_key, self.body.get("UZ", ""))
        if kwargs:
            title = title.format(**kwargs)
            body = body.format(**kwargs)
        return title, body


class NotificationMessages:
    order_created_msg = NotificationMessage(
        title={"UZ": "🆕 Yangi buyurtma", "RU": "🆕 Новый заказ", "EN": "🆕 New order"},
        body={
            "UZ": "Sizda #{order_id} sonli yangi buyurtma bor",
            "RU": "У вас новый заказ №#{order_id}",
            "EN": "You have a new order #{order_id}",
        },
        image={"UZ": None, "RU": None, "EN": None},
        type=NotificationType.ORDER_CREATED,
    )

    order_approved_msg = NotificationMessage(
        title={
            "UZ": "✅ Buyurtmangiz qabul qilindi",
            "RU": "✅ Заказ принят",
            "EN": "✅ Order accepted",
        },
        body={
            "UZ": "#{order_id} sonli buyurtmangiz administrator tomonidan tasdiqlandi.",
            "RU": "Ваш заказ №#{order_id} подтверждён администратором.",
            "EN": "Your order #{order_id} has been confirmed by admin.",
        },
        image={"UZ": None, "RU": None, "EN": None},
        type=NotificationType.ORDER_ACCEPTED,
    )

    order_rejected_msg = NotificationMessage(
        title={
            "UZ": "❌ Buyurtmangiz bekor qilindi",
            "RU": "❌ Заказ отменён",
            "EN": "❌ Order cancelled",
        },
        body={
            "UZ": "#{order_id} sonli buyurtmangiz bekor qilindi, {total_price} bal hisobingizga qaytarildi.",
            "RU": "Ваш заказ №#{order_id} отменён, {total_price} баллов возвращено на ваш баланс.",
            "EN": "Your order #{order_id} was cancelled, {total_price} points refunded to your balance.",
        },
        image={"UZ": None, "RU": None, "EN": None},
        type=NotificationType.ORDER_REJECTED,
    )

    order_completed_msg = NotificationMessage(
        title={
            "UZ": "🎉 Buyurtma yakunlandi",
            "RU": "🎉 Заказ завершён",
            "EN": "🎉 Order completed",
        },
        body={
            "UZ": "#{order_id} sonli buyurtmangiz muvaffaqiyatli yakunlandi.",
            "RU": "Ваш заказ №#{order_id} успешно завершён.",
            "EN": "Your order #{order_id} has been completed successfully.",
        },
        image={"UZ": None, "RU": None, "EN": None},
        type=NotificationType.ORDER_COMPLETED,
    )

    order_cancel_client_msg = NotificationMessage(
        title={"UZ": "❌ Mijoz bekor qildi", "RU": "❌ Клиент отменил", "EN": "❌ Customer canceled"},
        body={
            "UZ": "#{order_id} buyurtma mijoz tomonidan bekor qilindi",
            "RU": "Заказ №#{order_id} отменён клиентом",
            "EN": "Order #{order_id} was canceled by the customer",
        },
        image={"UZ": None, "RU": None, "EN": None},
        type=NotificationType.ORDER_CANCELED_BY_CLIENT,
    )

    bonus_create_msg = NotificationMessage(
        title={
            "UZ": "🎁 Bonus kod qabul qilindi",
            "RU": "🎁 Бонусный код принят",
            "EN": "🎁 Bonus code registered",
        },
        body={
            "UZ": "{code} kodi muvaffaqiyatli ro'yxatdan o'tkazildi. "
            "Tekshiruvdan so'ng hisobingizga {summa} bal qo'shiladi.",
            "RU": "Код {code} успешно зарегистрирован. "
            "После проверки на баланс будет начислено {summa} баллов.",
            "EN": "Code {code} was registered successfully. "
            "{summa} points will be credited to your balance after review.",
        },
        image={"UZ": None, "RU": None, "EN": None},
        type=NotificationType.BONUS_CODE_REGISTERED,
    )

    bonus_approved_msg = NotificationMessage(
        title={
            "UZ": "🎁 Bonus tasdiqlandi",
            "RU": "🎁 Бонус подтверждён",
            "EN": "🎁 Bonus approved",
        },
        body={
            "UZ": "Bonus kodingiz tasdiqlandi va hisobingizga {summa} bal qo'shildi.",
            "RU": "Ваш бонусный код подтверждён, на ваш баланс начислено {summa} баллов.",
            "EN": "Your bonus code was approved and {summa} points were credited to your balance.",
        },
        image={"UZ": None, "RU": None, "EN": None},
        type=NotificationType.BONUS_CLAIM_APPROVED,
    )

    bonus_rejected_msg = NotificationMessage(
        title={
            "UZ": "❌ Bonus bekor qilindi",
            "RU": "❌ Бонус отклонён",
            "EN": "❌ Bonus rejected",
        },
        body={
            "UZ": "Bonus kodingiz bekor qilindi. Sabab: {reason}",
            "RU": "Ваш бонусный код отклонён. Причина: {reason}",
            "EN": "Your bonus code was rejected. Reason: {reason}",
        },
        image={"UZ": None, "RU": None, "EN": None},
        type=NotificationType.BONUS_CLAIM_REJECTED,
    )

    challenge_completed_msg = NotificationMessage(
        title={
            "UZ": "🏆 Challenge yakunlandi",
            "RU": "🏆 Челлендж завершён",
            "EN": "🏆 Challenge completed",
        },
        body={
            "UZ": "Siz '{challenge_title}' challenge'ini muvaffaqiyatli yakunladingiz! "
            "Hisobingizga {reward} bal qo'shildi.",
            "RU": "Вы успешно завершили челлендж «{challenge_title}»! "
            "На ваш баланс начислено {reward} баллов.",
            "EN": "You successfully completed the '{challenge_title}' challenge! "
            "{reward} points were credited to your balance.",
        },
        image={"UZ": None, "RU": None, "EN": None},
        type=NotificationType.CHALLENGE_COMPLETED,
    )

    signup_bonus_msg = NotificationMessage(
        title={
            "UZ": "🎉 Xush kelibsiz!",
            "RU": "🎉 Добро пожаловать!",
            "EN": "🎉 Welcome!",
        },
        body={
            "UZ": "Ro'yxatdan o'tganingiz uchun hisobingizga {summa} so'm bonus berildi!",
            "RU": "Вам начислено {summa} сум бонуса за регистрацию!",
            "EN": "{summa} bonus was credited to your balance for signing up!",
        },
        image={"UZ": None, "RU": None, "EN": None},
        type=NotificationType.SIGNUP_BONUS,
    )

    points_expiring_warning_msg = NotificationMessage(
        title={
            "UZ": "⏳ Bonus muddati tugamoqda",
            "RU": "⏳ Срок действия баллов истекает",
            "EN": "⏳ Points expiring soon",
        },
        body={
            "UZ": "Sizning {summa} balingiz 7 kundan so'ng muddati tugaydi. Ularni sarflashga ulguring!",
            "RU": "Срок действия ваших {summa} баллов истекает через 7 дней. Успейте использовать!",
            "EN": "Your {summa} points will expire in 7 days. Be sure to use them!",
        },
        image={"UZ": None, "RU": None, "EN": None},
        type=NotificationType.POINTS_EXPIRING_WARNING,
    )

    points_expired_msg = NotificationMessage(
        title={
            "UZ": "⌛ Bonus muddati o'tdi",
            "RU": "⌛ Срок действия баллов истёк",
            "EN": "⌛ Points expired",
        },
        body={
            "UZ": "Amal qilish muddati (1 yil) tugaganligi sababli {summa} bal hisobingizdan chiqarildi.",
            "RU": "В связи с истечением срока действия (1 год) {summa} баллов списано с вашего баланса.",
            "EN": "{summa} points have been deducted due to expiration (1 year limit reached).",
        },
        image={"UZ": None, "RU": None, "EN": None},
        type=NotificationType.POINTS_EXPIRED,
    )
