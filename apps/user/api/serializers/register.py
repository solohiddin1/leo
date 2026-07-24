from rest_framework import serializers

from apps.user.models import User


class RegisterSerializer(serializers.ModelSerializer[User]):
    username = serializers.CharField(max_length=150)
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}