from rest_framework.generics import GenericAPIView

from apps.shared.permission.client import ClientPermission
from apps.shared.security import GeneralThrottle
from apps.user.api.serializers.set_password import SetPasswordSerializer
from apps.user.services.user_service import UserService


class SetPasswordAPIView(GenericAPIView):
    serializer_class = SetPasswordSerializer
    permission_classes = [ClientPermission]
    throttle_classes = [GeneralThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')
        return UserService.set_user_password(request.user, password)
