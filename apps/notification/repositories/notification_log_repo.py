from apps.notification.models import MarketingNotification, Notification, NotificationLog
from apps.user.models import Device, User


class NotificationLogRepo:
    @staticmethod
    def create(
        *,
        notification: Notification | None = None,
        marketing_notification: MarketingNotification | None = None,
        device: Device | None = None,
        user: User | None = None,
        status: str,
        fcm_message_id: str = "",
        error_message: str = "",
    ) -> NotificationLog:
        return NotificationLog.objects.create(
            notification=notification,
            marketing_notification=marketing_notification,
            device=device,
            user=user,
            status=status,
            fcm_message_id=fcm_message_id,
            error_message=error_message,
        )
