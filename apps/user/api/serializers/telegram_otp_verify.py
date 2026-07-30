from rest_framework import serializers

class TelegramOtpVerifySerializer(serializers.Serializer):
    token = serializers.CharField()
    otp = serializers.CharField()