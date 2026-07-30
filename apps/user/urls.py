from django.urls import path
from apps.user.api.views.register import RegisterAPIView
from apps.user.api.views.telegram_otp import TelegramOtpView, TelegramWebhookView, TelegramOtpPollView, TelegramOtpVerifyView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='index'),
    path('telegram_otp_request/', TelegramOtpView.as_view(), name='telegram_otp'),
    path('telegram_webhook/', TelegramWebhookView.as_view(), name='telegram_webhook'),
    path('telegram_otp_poll/', TelegramOtpPollView.as_view(), name='telegram_otp_poll'),
    path('telegram_otp_verify/', TelegramOtpVerifyView.as_view(), name='telegram_otp_verify'),
]