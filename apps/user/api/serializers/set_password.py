from rest_framework import serializers

from apps.user.models import User


class SetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    token = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
