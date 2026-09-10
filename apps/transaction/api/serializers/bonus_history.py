from rest_framework import serializers

from apps.product.api.serializers.products import ProductListSerializer
from apps.transaction.models import UserSumma, UserSummaImage


class UserSummaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSummaImage
        fields = ['id', 'image']


class UserSummaSerializer(serializers.ModelSerializer):
    code = serializers.StringRelatedField()
    store = serializers.StringRelatedField()
    product = ProductListSerializer(read_only=True)
    images = UserSummaImageSerializer(many=True, read_only=True)

    class Meta:
        model = UserSumma
        fields = [
            'id',
            'summa',
            'status',
            'code',
            'store',
            'product',
            'images',
            'rejection_reason',
            'reviewed_at',
            'created_at',
        ]
