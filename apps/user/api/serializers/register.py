from rest_framework import serializers

from apps.user.models import User


class RegisterSerializer(serializers.ModelSerializer[User]):
    username = serializers.CharField(max_length=150)
    device_id = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'password', 'device_id']
        extra_kwargs = {'password': {'write_only': True}}
