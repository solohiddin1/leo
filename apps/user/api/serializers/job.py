from rest_framework import serializers

from apps.user.models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title_uz', 'title_ru']