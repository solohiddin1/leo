from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.product.api.serializers.products import ProductListSerializer
from apps.transaction.models import Challenge


class ChallengeSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'product', 'target_count', 'reward_amount', 'start_date', 'end_date', 'progress']

    @extend_schema_field(serializers.DictField)
    def get_progress(self, obj):
        user = self.context['request'].user
        progress = obj.user_progress.filter(user=user).first()
        if progress:
            return {
                'current_count': progress.current_count,
                'is_completed': progress.is_completed
            }
        return {'current_count': 0, 'is_completed': False}
