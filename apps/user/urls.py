from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.api.views.job import JobsAPIView
from apps.user.api.views.login import LoginAPIView
from apps.user.api.views.profile import ProfileAPIView
from apps.user.api.views.register import RegisterAPIView
from apps.user.api.views.set_password import SetPasswordAPIView
from apps.user.api.views.telegram_otp import TelegramOtpView, TelegramWebhookView, TelegramOtpPollView, TelegramOtpVerifyView
from apps.user.api.views.profile import ProfileUpdateAPIView
from apps.user.api.views.logout import LogoutAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='index'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('telegram_otp_request/', TelegramOtpView.as_view(), name='telegram_otp'),
    path('telegram_webhook/', TelegramWebhookView.as_view(), name='telegram_webhook'),
    path('telegram_otp_poll/', TelegramOtpPollView.as_view(), name='telegram_otp_poll'),
    path('telegram_otp_verify/', TelegramOtpVerifyView.as_view(), name='telegram_otp_verify'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('set_password/', SetPasswordAPIView.as_view(), name='set_password'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('update_profile/', ProfileUpdateAPIView.as_view(), name='profile'),
    path('jobs/', JobsAPIView.as_view(), name='jobs'),
]