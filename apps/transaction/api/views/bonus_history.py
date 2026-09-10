from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import GenericAPIView

from apps.shared.permission.client import ClientPermission
from apps.shared.utils.paginator import CustomPagination
from apps.transaction.api.serializers.bonus_history import UserSummaSerializer
from apps.transaction.repositories.bonus_repo import BonusRepo
from apps.transaction.services.bonus_service import BonusService


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='status',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
        ),
        OpenApiParameter(
            name='search',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
        ),
        OpenApiParameter(
            name='from_datetime',
            type=OpenApiTypes.DATETIME,
            location=OpenApiParameter.QUERY,
            required=False,
        ),
        OpenApiParameter(
            name='to_datetime',
            type=OpenApiTypes.DATETIME,
            location=OpenApiParameter.QUERY,
            required=False,
        ),
        OpenApiParameter(
            name='store',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
        ),
    ]
)
class BonusHistoryView(GenericAPIView):
    permission_classes = [ClientPermission]
    serializer_class = UserSummaSerializer
    pagination_class = CustomPagination

    def get(self, request):
        claims = BonusService.get_user_bonuses(request.user, self.request)
        page = self.paginate_queryset(claims)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
