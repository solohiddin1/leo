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
        request={'multipart/form-data': BonusRedeemSerializer},
        responses={200: BonusRedeemResponseSerializer},
    )
    def post(self, request):
        raw_code = request.data.get('code', '').strip().upper()
        if not raw_code:
            return error_response(ResultCodes.BONUS_CODE_INVALID)

        bonus_code = BonusCode.objects.select_related('bonus').filter(code=raw_code).first()
        if not bonus_code:
            return error_response(ResultCodes.BONUS_CODE_NOT_FOUND)
        if bonus_code.is_used:
            return error_response(ResultCodes.BONUS_CODE_ALREADY_USED)

        images = request.FILES.getlist('images')

        user = request.user
        bonus = bonus_code.bonus

        user_summa = UserSumma.objects.create(
            user=user,
            bonus=bonus,
            code=raw_code,
            summa=bonus.summa,
        )

        if images:
            UserSummaImage.objects.bulk_create([
                UserSummaImage(user_summa=user_summa, image=img) for img in images
            ])

        bonus_code.is_used = True
        bonus_code.save(update_fields=['is_used'])

        user.balance += bonus.summa
        user.save(update_fields=['balance'])

        return success_response({'balance': user.balance, 'awarded': bonus.summa})