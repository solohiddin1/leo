from rest_framework import serializers


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    device_id = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Device.device_id of the device logging out; its push token is deactivated if provided.",
    )
