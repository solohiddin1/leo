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


class ProfileUpdateAPIView(GenericAPIView):
    permission_classes = [ClientPermission]
    serializer_class = SetProfileSerializer
    throttle_classes = [GeneralThrottle]


    def patch(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(serializer.data)
