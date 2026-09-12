from rest_framework import serializers


class LeaderboardSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    total_earned = serializers.IntegerField()
    rank = serializers.IntegerField()
    is_me = serializers.BooleanField(help_text="True for the requesting user's own row.")
