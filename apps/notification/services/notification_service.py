from firebase_admin import messaging

from apps.notification.models import MarketingNotification, Notification
from apps.notification.repositories.notification_log_repo import NotificationLogRepo
from apps.notification.repositories.notification_repo import NotificationRepo
from apps.notification.services.firebase_service import FirebaseService
from apps.shared.utils.result_codes import ResultCodes
from apps.shared.utils.utils import error_response, success_response
from apps.user.models import Device, User
from apps.user.repositories.device_repo import DeviceRepo


class NotificationService:
    @staticmethod
    def mark_as_read(user: User, notification_id: int):
        notification = NotificationRepo.get_by_id(notification_id, user)
        if notification is None:
            return error_response(ResultCodes.NOTIFICATION_NOT_FOUND)
        NotificationRepo.mark_as_read(notification)
        return success_response(ResultCodes.SUCCESS)

    @staticmethod
    def read_all(user: User):
        notifications = NotificationRepo.get_all_by_user(user)
        if notifications is None:
            return error_response(ResultCodes.NOTIFICATION_NOT_FOUND)
        NotificationRepo.read_all(notifications)
        return success_response(ResultCodes.SUCCESS)

    @staticmethod
    def send_to_user(
        user: User,
        title: str,
        body: str,
        notification_type: str = "SYSTEM",
        data: dict | None = None,
    ) -> Notification:
        notification = NotificationRepo.create(user, title, body, notification_type, data)
        for device in DeviceRepo.get_user_active_devices(user):
            NotificationService._push_to_device(notification, None, device, title, body, data)
        return notification

    @staticmethod
    def _push_to_device(
        notification: Notification | None,
        marketing_notification: MarketingNotification | None,
        device: Device,
        title: str,
        body: str,
        data: dict | None,
    ) -> None:
        try:
            message_id = FirebaseService.send_to_token(device.fcm_token, title, body, data)
            NotificationLogRepo.create(
                notification=notification,
                marketing_notification=marketing_notification,
                device=device,
                user=device.user,
                status="SUCCESS",
                fcm_message_id=message_id,
            )
        except messaging.UnregisteredError as exc:
            DeviceRepo.deactivate(device)
            NotificationLogRepo.create(
                notification=notification,
                marketing_notification=marketing_notification,
                device=device,
                user=device.user,
                status="FAILED",
                error_message=str(exc),
            )
        except Exception as exc:
            NotificationLogRepo.create(
                notification=notification,
                marketing_notification=marketing_notification,
                device=device,
                user=device.user,
                status="FAILED",
                error_message=str(exc),
            )
