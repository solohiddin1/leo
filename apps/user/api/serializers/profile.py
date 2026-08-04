from rest_framework import serializers

from apps.user.models import User


class ProfileSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True, allow_null=True)
    region_name = serializers.CharField(source='region.name_uz', read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'region_id', 'region_name', 'job_id', 'job_title']


class SetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'region', 'job']
    # region_id = serializers.IntegerField(required=False, allow_null=True)
    # job_id = serializers.IntegerField(required=False, allow_null=True)