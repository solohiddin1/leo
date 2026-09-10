from django.utils import timezone
from rest_framework.generics import GenericAPIView

from apps.shared.permission.client import ClientPermission
from apps.shared.utils.utils import success_response
from apps.transaction.api.serializers.challenges import ChallengeSerializer
from apps.transaction.repositories.challenge_repo import ChallengeRepo


class ChallengeListView(GenericAPIView):
    permission_classes = [ClientPermission]
    serializer_class = ChallengeSerializer

    def get(self, request):
        challenges = ChallengeRepo.get_visible(timezone.now())
        serialized = self.get_serializer(challenges, many=True).data
        return success_response(serialized)
