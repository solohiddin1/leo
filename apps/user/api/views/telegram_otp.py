from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.shared.utils.result_codes import ResultCodes
from apps.shared.utils.utils import success_response, error_response
from apps.user.api.serializers.telegram_otp_verify import TelegramOtpVerifySerializer
from apps.user.services.telegram import TgOtpService


class TelegramOtpView(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            return success_response(TgOtpService.request())
        except Exception as e:
            return error_response(ResultCodes.UNKNOWN_ERROR, {
                "en": str(e),
                "ru": str(e),
                "uz": str(e)
            })


class TelegramWebhookView(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print("Telegram Webhook Data:", request.data)
        TgOtpService.handle_update(request.data)
        return Response({"ok": True})


class TelegramOtpPollView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        token = request.query_params.get("token")
        if not token:
            return error_response(ResultCodes.UNKNOWN_ERROR, {
                "en": "token required", "ru": "token required", "uz": "token required"
            })
        result = TgOtpService.poll(token)
        return success_response(result)


class TelegramOtpVerifyView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = TelegramOtpVerifySerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("id")
        otp = request.data.get("otp")
        if not user_id or not otp:
            return error_response(ResultCodes.UNKNOWN_ERROR, {
                "en": "token and otp required", "ru": "token and otp required", "uz": "token va otp talab qilinadi"
            })
        result = TgOtpService.verify_otp(user_id, otp)
        if "error" in result:
            return error_response(ResultCodes.UNKNOWN_ERROR, {
                "en": result["error"], "ru": result["error"], "uz": result["error"]
            })
        return success_response(result)
