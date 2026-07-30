from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle

from apps.user.models import User
from apps.user.services.user_service import UserService
from apps.user.api.serializers.register import RegisterSerializer


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserService.register(serializer.data)
