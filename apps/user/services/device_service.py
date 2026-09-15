from apps.shared.utils.result_codes import ResultCodes
from apps.shared.utils.utils import error_response, success_response
from apps.user.models import User
from apps.user.repositories.device_repo import DeviceRepo
from apps.user.api.serializers.device_add import DeviceSerializer


class DeviceService:
    @staticmethod
    def add_device(
        user: User, name: str, device_type: str, device_id: str, fcm_token: str = ""
    ):

        device = DeviceRepo.add_device(user, name, device_type, device_id, fcm_token)
        return success_response(DeviceSerializer(device).data)

    @staticmethod
    def delete_device(user: User, device_id: int):
        device = DeviceRepo.get_active_by_id(device_id, user)
        if device is None:
            return error_response(ResultCodes.DEVICE_NOT_FOUND)
        DeviceRepo.deactivate(device)
        return success_response(ResultCodes.SUCCESS)

    @staticmethod
    def deactivate_by_device_id(user: User, device_id: str) -> None:
        device = DeviceRepo.get_active_by_device_id(device_id, user)
        if device is not None:
            DeviceRepo.deactivate(device)
