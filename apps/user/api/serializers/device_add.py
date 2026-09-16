from rest_framework import serializers

from apps.user.models import Device


class DeviceAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["name", "device_type", "device_id", "fcm_token"]
        extra_kwargs = {"fcm_token": {"required": False}}


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["id", "name", "device_type", "device_id", "is_active", "created_at"]
