from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.shared.models import TrainingVideo, TrainingVideoStatus


class TrainingVideoSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    is_mine = serializers.SerializerMethodField()

    class Meta:
        model = TrainingVideo
        fields = [
            "id",
            "name_uz",
            "name_ru",
            "description_uz",
            "description_ru",
            "youtube_url",
            "file",
            "ordering",
            "is_active",
            "status",
            "is_mine",
            "created_at",
        ]

    @extend_schema_field(serializers.BooleanField)
    def get_is_mine(self, obj) -> bool:
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            return obj.user_id == request.user.id
        return False


class TrainingVideoUploadSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    file = serializers.FileField(required=False, allow_null=True)
    youtube_url = serializers.CharField(max_length=500, required=False, allow_blank=True, default="")

    class Meta:
        model = TrainingVideo
        fields = ["id", "name", "description", "file", "youtube_url", "status", "created_at"]
        read_only_fields = ["id", "status", "created_at"]

    def validate(self, attrs):
        file = attrs.get("file")
        youtube_url = (attrs.get("youtube_url") or "").strip()
        if not file and not youtube_url:
            raise serializers.ValidationError(
                "Kamida video fayl yoki YouTube havola kiritilishi kerak."
            )
        if file and file.size > 200 * 1024 * 1024:
            raise serializers.ValidationError(
                "Video fayl hajmi 200 MB dan oshmasligi kerak."
            )
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        name = validated_data.pop("name", "")
        desc = validated_data.pop("description", "")
        validated_data.pop("name_uz", None)
        validated_data.pop("name_ru", None)
        validated_data.pop("description_uz", None)
        validated_data.pop("description_ru", None)

        return TrainingVideo.objects.create(
            user=user,
            status=TrainingVideoStatus.PENDING,
            name=name,
            name_uz=name,
            name_ru=name,
            description=desc,
            description_uz=desc,
            description_ru=desc,
            **validated_data,
        )
