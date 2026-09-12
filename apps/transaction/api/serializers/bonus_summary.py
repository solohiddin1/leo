from rest_framework import serializers


class BonusSummarySerializer(serializers.Serializer):
    balance = serializers.IntegerField()
    pending_balance = serializers.IntegerField()
    total_earned = serializers.IntegerField()
