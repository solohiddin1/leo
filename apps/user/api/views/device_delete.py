from rest_framework.generics import GenericAPIView

from apps.shared.permission.client import ClientPermission
from apps.user.models import Device
from apps.user.services.device_service import DeviceService


class DeviceDeleteView(GenericAPIView):
    permission_classes = [ClientPermission]
    queryset = Device.objects.all()

    def delete(self, request, *args, **kwargs):
        return DeviceService.delete_device(request.user, kwargs["device_id"])
