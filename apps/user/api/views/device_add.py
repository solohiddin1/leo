from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from apps.shared.permission.client import ClientPermission
from apps.user.api.serializers.device_add import DeviceAddSerializer
from apps.user.models import Device


class DeviceAddView(GenericAPIView):
    permission_classes = [ClientPermission]
    serializer_class = DeviceAddSerializer
    queryset = Device.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        device = serializer.save(is_active=True)
        device.save()