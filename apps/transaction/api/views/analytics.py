from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView

from apps.shared.permission.client import ClientPermission
from apps.shared.utils.utils import success_response
from apps.transaction.services.analytics_service import AnalyticsService


@extend_schema(exclude=True)
class AnalyticsView(GenericAPIView):
    permission_classes = [ClientPermission]

    def get(self, request):
        return success_response(AnalyticsService.get_user_claim_stats(request.user))
