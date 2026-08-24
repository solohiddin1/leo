from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.shared.utils.result_codes import ResultCodes
from apps.shared.utils.utils import error_response, success_response
from apps.transaction.api.serializers.bonus import (
    BonusCheckQuerySerializer,
    BonusCheckResponseSerializer,
    BonusRedeemResponseSerializer,
    BonusRedeemSerializer,
)
from apps.transaction.models import BonusCode, UserSumma, UserSummaImage
from apps.transaction.services import BonusService
from apps.shared.models import SiteConfig


class RequiredImagesView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: {'type': 'object', 'properties': {'count': {'type': 'integer'}}}}
    )
    def get(self, request):
        config = SiteConfig.objects.first()
        count = config.required_bonus_images_count if config else 1
        return success_response({'count': count})


class CheckCodeView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[OpenApiParameter(name='code', type=str, location=OpenApiParameter.QUERY, required=True)],
        responses={200: BonusCheckResponseSerializer},
    )
    def get(self, request):
        raw_code = request.query_params.get('code', '').strip().upper()
        if not raw_code:
            return error_response(ResultCodes.BONUS_CODE_INVALID)

        bonus_code = BonusCode.objects.select_related('bonus').filter(code=raw_code).first()
        if not bonus_code:
            return error_response(ResultCodes.BONUS_CODE_NOT_FOUND)
        if bonus_code.is_used:
            return error_response(ResultCodes.BONUS_CODE_ALREADY_USED)

        return success_response({'summa': bonus_code.bonus.summa})

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'string'},
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
            images=request.FILES.getlist('images')
        )