from rest_framework import serializers

from apps.user.models import User


class LoginSerializer(serializers.ModelSerializer[User]):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, value: str) -> str:
        if value:
            return value.strip().replace("+", "")
        return value
