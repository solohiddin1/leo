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
            "lang",
        ]


class UserLangUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["lang"]


class UserProfileImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["avatar"]

    def validate_avatar(self, value):
        max_size = 10 * 1024 * 1024  # 10 MB
        if value and value.size > max_size:
            raise serializers.ValidationError("Avatar image size cannot exceed 10 MB.")
        return value
