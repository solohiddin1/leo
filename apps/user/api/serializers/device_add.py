from rest_framework import serializers
from apps.user.models import Device

class DeviceAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['name', 'device_type', 'device_id', 'fcm_token']