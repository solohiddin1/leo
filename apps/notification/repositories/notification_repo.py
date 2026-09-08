from django.db.models import QuerySet

from apps.notification.models import MarketingNotification, Notification
from apps.user.models import User


class NotificationRepo:
    @staticmethod
    def get_user_notifications(user: User) -> QuerySet[Notification]:
        return Notification.objects.filter(user=user)

    @staticmethod
    def get_by_id(notification_id: int, user: User) -> Notification | None:
        return Notification.objects.filter(id=notification_id, user=user).first()

    @staticmethod
    def get_all_by_user(user: User) -> QuerySet[Notification] | None:
        return Notification.objects.filter(user=user)

    @staticmethod
    def create(
        user: User,
        title: str,
        body: str,
        notification_type: str = "SYSTEM",
        data: dict | None = None,
        image=None,
        marketing_notification: MarketingNotification | None = None,
    ) -> Notification:
        return Notification.objects.create(
            user=user,
            title=title,
            body=body,
            notification_type=notification_type,
            data=data or {},
            image=image,
            marketing_notification=marketing_notification,
        )

    @staticmethod
    def mark_as_read(notification: Notification) -> Notification:
        notification.is_read = True
        notification.save(update_fields=["is_read"])
        return notification

    @staticmethod
    def read_all(notifications: QuerySet[Notification]) -> bool:
        updated_count = notifications.update(is_read=True)
        return updated_count > 0
