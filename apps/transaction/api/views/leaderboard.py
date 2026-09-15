from rest_framework.generics import GenericAPIView

from apps.shared.permission.client import ClientPermission
from apps.transaction.api.serializers.leaderboard import LeaderboardSerializer
from apps.transaction.services.leaderboard_service import LeaderboardService


class LeaderboardView(GenericAPIView):
    permission_classes = [ClientPermission]
    serializer_class = LeaderboardSerializer

    def get(self, request):
        return LeaderboardService.get_leaderboard(request.user)
