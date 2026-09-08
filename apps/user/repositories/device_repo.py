from django.db.models import QuerySet

from apps.user.models import Device, User


class DeviceRepo:
    @staticmethod
    def get_active_by_id(device_id: int, user: User) -> Device | None:
        return Device.objects.filter(id=device_id, user=user, is_active=True).first()

    @staticmethod
    def get_active_by_device_id(device_id: str, user: User) -> Device | None:
        return Device.objects.filter(device_id=device_id, user=user, is_active=True).first()

    @staticmethod
    def get_user_active_devices(user: User) -> QuerySet[Device]:
        return Device.objects.filter(user=user, is_active=True).exclude(fcm_token="")

    @staticmethod
    def get_active_devices_for_audience(audience: str) -> QuerySet[Device]:
        qs = Device.objects.filter(is_active=True).exclude(fcm_token="").exclude(user__isnull=True)
        if audience and audience != "ALL":
            qs = qs.filter(device_type=audience)
        return qs.select_related("user")

    @staticmethod
    def add_device(
        user: User, name: str, device_type: str, device_id: str, fcm_token: str = ""
    ) -> Device:
        device, _ = Device.objects.update_or_create(
            user=user,
            device_id=device_id,
            defaults={
                "name": name,
                "device_type": device_type,
                "fcm_token": fcm_token,
                "is_active": True,
            },
        )
        return device

    @staticmethod
    def deactivate(device: Device) -> Device:
        device.is_active = False
        device.save(update_fields=["is_active"])
        return device
