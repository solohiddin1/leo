from rest_framework import serializers

from apps.transaction.models import UserSumma


class UserSummaSerializer(serializers.ModelSerializer):
    code = serializers.StringRelatedField()
    store = serializers.StringRelatedField()

    class Meta:
        model = UserSumma
        fields = ['id', 'summa', 'status', 'code', 'store', 'rejection_reason', 'reviewed_at', 'created_at']
