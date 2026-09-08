from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.transaction.api.serializers.leaderboard import LeaderboardSerializer
from apps.transaction.services.leaderboard_service import LeaderboardService


class LeaderboardView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LeaderboardSerializer

    def get(self, request):
        return LeaderboardService.get_leaderboard(request.user)
