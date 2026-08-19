from rest_framework import serializers

from apps.user.api.serializers.job import JobSerializer
from apps.user.api.serializers.region import RegionSerializer
from apps.user.models import User


class ProfileSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    region = RegionSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "main_balance",
            "balance",
            "telegram_username",
            "lang",
            "region",
            "job",
        ]


class SetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "region",
            "job",
        ]
