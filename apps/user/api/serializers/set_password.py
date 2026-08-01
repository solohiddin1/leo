from rest_framework import serializers


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=150)
