from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.transaction.api.serializers.check_code import (
    BonusCheckResponseSerializer,
    BonusRedeemResponseSerializer,
    BonusRedeemSerializer,
)
from apps.transaction.services.bonus_service import BonusService


class CheckCodeView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[OpenApiParameter(name='code', type=str, location=OpenApiParameter.QUERY, required=True)],
        responses={200: BonusCheckResponseSerializer},
    )
    def get(self, request):
        raw_code = request.query_params.get('code', '')
        return BonusService.check_code(raw_code)

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'string'},
                    'store_id': {'type': 'string'},
                    'images': {
                        'type': 'array',
                        'items': {'type': 'string', 'format': 'binary'}
                    },
                },
            }
        },
        responses={200: BonusRedeemResponseSerializer},
    )
    def post(self, request):
        serializer = BonusRedeemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return BonusService.redeem_bonus(
            user=request.user,
            raw_code=serializer.validated_data['code'],
            store_id=serializer.validated_data['store_id'],
            images=request.FILES.getlist('images')
        )
