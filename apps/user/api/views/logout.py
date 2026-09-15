from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.shared.permission.client import ClientPermission
from apps.shared.security import GeneralThrottle
from apps.shared.utils.result_codes import ResultCodes
from apps.shared.utils.utils import error_response, success_response
from apps.user.api.serializers.logout import LogoutSerializer
from apps.user.models import User
from apps.user.services.device_service import DeviceService


class LogoutAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LogoutSerializer
    permission_classes = [ClientPermission]
    throttle_classes = [GeneralThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            RefreshToken(serializer.validated_data["refresh_token"]).blacklist()
        except TokenError:
            return error_response(ResultCodes.INVALID_TOKEN_ERROR)

        device_id = serializer.validated_data.get("device_id")
        if device_id:
            DeviceService.deactivate_by_device_id(request.user, device_id)

        return success_response()
