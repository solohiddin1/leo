from rest_framework import serializers

class TelegramOtpVerifySerializer(serializers.Serializer):
    id = serializers.CharField()
    otp = serializers.CharField()