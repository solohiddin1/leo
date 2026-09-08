from rest_framework import serializers

from apps.transaction.models import Challenge


class ChallengeSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'target_count', 'reward_amount', 'start_date', 'end_date', 'progress']

    def get_progress(self, obj):
        user = self.context['request'].user
        progress = obj.user_progress.filter(user=user).first()
        if progress:
            return {
                'current_count': progress.current_count,
                'is_completed': progress.is_completed
            }
        return {'current_count': 0, 'is_completed': False}
