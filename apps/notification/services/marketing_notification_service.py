from django.utils import timezone

from apps.notification.models import MarketingNotification
from apps.notification.repositories.notification_repo import NotificationRepo
from apps.notification.services.notification_service import NotificationService
from apps.user.repositories.device_repo import DeviceRepo


class MarketingNotificationService:
    @staticmethod
    def send(marketing_notification: MarketingNotification) -> MarketingNotification:
        devices = list(DeviceRepo.get_active_devices_for_audience(marketing_notification.audience))

        marketing_notification.status = "SENDING"
        marketing_notification.total_targets = len(devices)
        marketing_notification.save(update_fields=["status", "total_targets"])

        for device in devices:
            notification = NotificationRepo.create(
                user=device.user,
                title=marketing_notification.title,
                body=marketing_notification.body,
                notification_type="MARKETING",
                data=marketing_notification.data,
                marketing_notification=marketing_notification,
            )
            NotificationService._push_to_device(
                notification,
                marketing_notification,
                device,
                marketing_notification.title,
                marketing_notification.body,
                marketing_notification.data,
            )

        logs = marketing_notification.logs.all()
        sent_count = logs.filter(status="SUCCESS").count()
        failed_count = logs.filter(status="FAILED").count()

        marketing_notification.sent_count = sent_count
        marketing_notification.failed_count = failed_count
        marketing_notification.status = "FAILED" if sent_count == 0 and failed_count > 0 else "SENT"
        marketing_notification.sent_at = timezone.now()
        marketing_notification.save(
            update_fields=["sent_count", "failed_count", "status", "sent_at"]
        )
        return marketing_notification
