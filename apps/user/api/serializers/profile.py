from rest_framework import serializers

from apps.user.api.serializers.job import JobSerializer
from apps.user.api.serializers.region import RegionSerializer
from apps.user.models import Avatar, User


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ["id", "name", "image"]


class ProfileSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    region = RegionSerializer()
    avatar = AvatarSerializer()

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
            "avatar",
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
