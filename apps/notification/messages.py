from dataclasses import dataclass
from enum import IntEnum


class NotificationType(IntEnum):
    ORDER_CREATED = 1
    ORDER_CANCELED_BY_CLIENT = 2
    BONUS_CODE_REGISTERED = 3
    CHALLENGE_COMPLETED = 4


@dataclass(frozen=True)
class NotificationMessage:
    title: dict[str, str]
    body: dict[str, str]
    image: dict[str, str | None]
    type: NotificationType

    def render(self, lang: str | None, **kwargs) -> tuple[str, str]:
        lang_key = (lang or "UZ").upper()
        title = self.title.get(lang_key, self.title["UZ"])
        body = self.body.get(lang_key, self.body["UZ"])
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
            "Tekshiruvdan so'ng hisobingizga {summa} so'm qo'shiladi.",
            "RU": "Код {code} успешно зарегистрирован. "
            "После проверки на баланс будет начислено {summa}.",
            "EN": "Code {code} was registered successfully. "
            "{summa} will be credited to your balance after review.",
        },
        image={"UZ": None, "RU": None, "EN": None},
        type=NotificationType.BONUS_CODE_REGISTERED,
    )

    challenge_completed_msg = NotificationMessage(
        title={
            "UZ": "🏆 Challenge yakunlandi",
            "RU": "🏆 Челлендж завершён",
            "EN": "🏆 Challenge completed",
        },
        body={
            "UZ": "Siz '{challenge_title}' challenge'ini muvaffaqiyatli yakunladingiz! "
            "Hisobingizga {reward} so'm qo'shildi.",
            "RU": "Вы успешно завершили челлендж «{challenge_title}»! "
            "На ваш баланс начислено {reward}.",
            "EN": "You successfully completed the '{challenge_title}' challenge! "
            "{reward} was credited to your balance.",
        },
        image={"UZ": None, "RU": None, "EN": None},
        type=NotificationType.CHALLENGE_COMPLETED,
    )
