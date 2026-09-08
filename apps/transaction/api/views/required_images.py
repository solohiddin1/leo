from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.shared.utils.utils import success_response
from apps.transaction.services.bonus_service import BonusService


class RequiredImagesView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: {'type': 'object', 'properties': {'count': {'type': 'integer'}}}}
    )
    def get(self, request):
        return success_response({'count': BonusService.get_required_images_count()})
