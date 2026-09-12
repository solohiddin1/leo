from rest_framework import serializers

from apps.shared.models import Store
from apps.user.api.serializers.region import RegionSerializer


class StoreSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Store
        fields = [
            "id",
            "name",
            "address",
            "region",
            "phone_number",
            "lat",
            "long",
            "is_priority",
            "bonus_boost_percentage",
        ]
