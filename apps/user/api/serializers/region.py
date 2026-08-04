from rest_framework import serializers

from apps.shared.models import Region


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'soato_id', 'name_uz', 'name_ru', 'name_en', 'ordering']