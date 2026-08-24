from django.db import transaction
from apps.transaction.models import BonusCode, UserSumma, UserSummaImage
from apps.shared.models import SiteConfig
from apps.shared.utils.result_codes import ResultCodes
from apps.shared.utils.utils import error_response, success_response

class BonusService:
    @staticmethod
    def redeem_bonus(user, raw_code: str, images=None):
        raw_code = raw_code.strip().upper()
        
        config = SiteConfig.objects.first()
        required_count = config.required_bonus_images_count if config else 1
        
        images = images or []
        if len(images) < required_count:
            return error_response(ResultCodes.BONUS_CODE_IMAGE_REQUIRED)

        with transaction.atomic():
            bonus_code = BonusCode.objects.select_related('bonus').select_for_update().filter(code=raw_code).first()
            
            if not bonus_code:
                return error_response(ResultCodes.BONUS_CODE_NOT_FOUND)
            
            if bonus_code.is_used:
                return error_response(ResultCodes.BONUS_CODE_ALREADY_USED)
            
            bonus = bonus_code.bonus
            if not bonus:
                return error_response(ResultCodes.BONUS_CODE_INVALID)

            user_summa = UserSumma.objects.create(
                user=user,
                bonus=bonus,
                code=bonus_code,
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

            return success_response({
                'balance': user.balance, 
                'awarded': bonus.summa
            })
