from rest_framework import serializers

from apps.shared.models import Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ["id", "name", "image", "image_compressed", "url", "ordering"]
