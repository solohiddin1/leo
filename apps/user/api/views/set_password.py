from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from apps.shared.security import GeneralThrottle
from apps.user.api.serializers.login import LoginSerializer
from apps.user.models import User
from apps.user.services.user_service import UserService


class SetPasswordAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    throttle_classes = [GeneralThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        return UserService.login(username, password)
