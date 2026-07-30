from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle
from apps.user.services.user_service import UserService

class VerifyOTPAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        otp = request.data.get('otp')
        phone_number = request.data.get('phone_number')

        return UserService.verify_otp(phone_number, otp)
