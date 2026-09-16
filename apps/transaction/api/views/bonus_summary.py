from rest_framework.generics import GenericAPIView

from apps.shared.permission.client import ClientPermission
from apps.transaction.api.serializers.bonus_summary import BonusSummarySerializer
from apps.transaction.services.bonus_service import BonusService


class BonusSummaryView(GenericAPIView):
    permission_classes = [ClientPermission]
    serializer_class = BonusSummarySerializer

    def get(self, request):
        return BonusService.get_summary(request.user)
