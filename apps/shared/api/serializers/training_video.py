from rest_framework import serializers

from apps.shared.models import TrainingVideo


class TrainingVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingVideo
        fields = [
            "id",
            "name",
            "name_uz",
            "name_ru",
            "description",
            "description_uz",
            "description_ru",
            "youtube_url",
            "file",
            "ordering",
            "is_active",
            "created_at",
        ]
