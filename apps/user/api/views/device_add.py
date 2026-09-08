from rest_framework.generics import GenericAPIView

from apps.shared.permission.client import ClientPermission
from apps.user.api.serializers.device_add import DeviceAddSerializer
from apps.user.models import Device
from apps.user.services.device_service import DeviceService


class DeviceAddView(GenericAPIView):
    permission_classes = [ClientPermission]
    serializer_class = DeviceAddSerializer
    queryset = Device.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return DeviceService.add_device(request.user, **serializer.validated_data)
