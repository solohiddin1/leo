from rest_framework import serializers

from apps.user.models import User
from user.api.serializers.job import JobSerializer
from user.api.serializers.region import RegionSerializer


class ProfileSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    region = RegionSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'main_balance',
            'balance',
            'telegram_username',
            'lang',
            'region',
            'job',
          ]


class SetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'region',
            'job',
        ]
