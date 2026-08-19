import re

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.shared.utils.result_codes import ResultCodes
from apps.shared.utils.utils import error_response, success_response
from apps.transaction.models import Bonus, UserSumma


def _parse_code(raw_code):
    """
    Returns (canonical_code, typed_code) or raises ValueError.
    Format: {prefix}{checksum_letter}{serial:04d}
    Checksum rule: ord(letter) - ord('A') == serial % 26
    """
    code = raw_code.strip().upper()
    m = re.match(r'^(.*?)([A-Z])(\d{4})$', code)
    if not m:
        raise ValueError("invalid format")

    prefix, checksum_letter, serial_str = m.group(1), m.group(2), m.group(3)
    serial = int(serial_str)

    if ord(checksum_letter) != ord('A') + (serial % 26):
        raise ValueError("checksum mismatch")

    canonical = prefix + 'A' + '0000'
    return canonical, code


class CheckCodeView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        raw_code = request.query_params.get('code', '')
        if not raw_code:
            return error_response(ResultCodes.BONUS_CODE_INVALID)

        try:
            canonical, typed_code = _parse_code(raw_code)
        except ValueError:
            return error_response(ResultCodes.BONUS_CODE_INVALID)

        if UserSumma.objects.filter(code=typed_code).exists():
            return error_response(ResultCodes.BONUS_CODE_ALREADY_USED)

        if not Bonus.objects.filter(code=canonical).exists():
            return error_response(ResultCodes.BONUS_CODE_NOT_FOUND)

        return success_response()

    def post(self, request):
        raw_code = request.data.get('code', '')
        if not raw_code:
            return error_response(ResultCodes.BONUS_CODE_INVALID)

        try:
            canonical, typed_code = _parse_code(raw_code)
        except ValueError:
            return error_response(ResultCodes.BONUS_CODE_INVALID)

        if UserSumma.objects.filter(code=typed_code).exists():
            return error_response(ResultCodes.BONUS_CODE_ALREADY_USED)

        bonus = Bonus.objects.filter(code=canonical).first()
        if not bonus:
            return error_response(ResultCodes.BONUS_CODE_NOT_FOUND)

        user = request.user
        UserSumma.objects.create(
            user=user,
            bonus=bonus,
            code=typed_code,
            summa=bonus.summa,
        )
        user.balance += bonus.summa
        user.save(update_fields=['balance'])

        return success_response({'balance': user.balance, 'awarded': bonus.summa})
