from rest_framework.generics import GenericAPIView

from apps.shared.permission.client import ClientPermission
from apps.shared.security import GeneralThrottle
from apps.shared.utils.utils import success_response
from apps.user.api.serializers.profile import ProfileSerializer, SetProfileSerializer
from apps.user.services.user_service import UserService


class ProfileAPIView(GenericAPIView):
    permission_classes = [ClientPermission]
    serializer_class = ProfileSerializer
    throttle_classes = [GeneralThrottle]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return success_response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = SetProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserService.set_profile(request.user, serializer.validated_data)
