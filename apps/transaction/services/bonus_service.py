from django.core.cache import cache
from django.db import transaction
from django.utils import timezone

from apps.shared.models import SiteConfig
from apps.shared.repositories.store_repo import StoreRepo
from apps.shared.utils.result_codes import ResultCodes
from apps.shared.utils.utils import error_response, success_response
from apps.transaction.models import BonusClaimStatus, BonusCode
from apps.transaction.repositories.bonus_repo import BonusRepo
from apps.transaction.repositories.challenge_repo import ChallengeRepo
from apps.user.models import User


class BonusService:
    PENDING_BALANCE_CACHE_KEY = "user_{user_id}_pending_balance"
    TOTAL_EARNED_CACHE_KEY = "user_{user_id}_total_earned"
    CACHE_TIMEOUT = 3600  # 1 hour

    @staticmethod
    def _clear_user_balance_cache(user_id: int):
        cache.delete(BonusService.PENDING_BALANCE_CACHE_KEY.format(user_id=user_id))
        cache.delete(BonusService.TOTAL_EARNED_CACHE_KEY.format(user_id=user_id))

    @staticmethod
    def get_required_images_count() -> int:
        return 3

    @staticmethod
    def check_code(raw_code: str):
        raw_code = raw_code.strip().upper()
        if not raw_code:
            return error_response(ResultCodes.BONUS_CODE_INVALID)

        bonus_code = BonusRepo.get_by_code(raw_code)
        if not bonus_code:
            return error_response(ResultCodes.BONUS_CODE_NOT_FOUND)
        if bonus_code.is_used:
            return error_response(ResultCodes.BONUS_CODE_ALREADY_USED)

        return success_response({'summa': bonus_code.bonus.summa})

    @staticmethod
    def redeem_bonus(user: User, raw_code: str, store_id: int, images=None):
        raw_code = raw_code.strip().upper()

        required_count = BonusService.get_required_images_count()

        images = images or []
        if len(images) < required_count:
            return error_response(ResultCodes.BONUS_CODE_IMAGE_REQUIRED)

        with transaction.atomic():
            bonus_code = BonusRepo.lock_by_code(raw_code)

            if not bonus_code:
                return error_response(ResultCodes.BONUS_CODE_NOT_FOUND)

            if bonus_code.is_used:
                return error_response(ResultCodes.BONUS_CODE_ALREADY_USED)

            bonus = bonus_code.bonus
            if not bonus:
                return error_response(ResultCodes.BONUS_CODE_INVALID)

            store = StoreRepo.get_by_id(store_id)
            if not store:
                return error_response(ResultCodes.STORE_NOT_FOUND)

            user_summa = BonusRepo.create_claim(user, bonus, bonus_code, store)

            if images:
                BonusRepo.bulk_create_images(user_summa, images)

            BonusRepo.mark_used(bonus_code)

            BonusService._clear_user_balance_cache(user.id)

            transaction.on_commit(
                lambda: BonusService._notify_bonus_code_registered(user, bonus_code, bonus)
            )

            return success_response({
                'balance': user.balance,
                'pending_balance': BonusService.get_user_pending_balance(user),
                'awarded': bonus.summa
            })

    @staticmethod
    def _notify_bonus_code_registered(user: User, bonus_code: BonusCode, bonus) -> None:
        from apps.notification.messages import NotificationMessages
        from apps.notification.services.notification_service import NotificationService

        msg = NotificationMessages.bonus_create_msg
        title, body = msg.render(user.lang, code=bonus_code.code, summa=bonus.summa)
        NotificationService.send_to_user(
            user=user,
            title=title,
            body=body,
            notification_type="BONUS",
            data={
                "type": msg.type.value,
                "code": bonus_code.code,
                "awarded": bonus.summa,
                "status": BonusClaimStatus.PENDING,
            },
        )

    @staticmethod
    def approve_claim(claim_id: int, admin_user: User):
        from apps.transaction.services.challenge_service import ChallengeService

        with transaction.atomic():
            claim = BonusRepo.get_pending_claim(claim_id)
            if not claim:
                return error_response(ResultCodes.CLAIM_NOT_FOUND)

            user = claim.user
            BonusRepo.approve(claim, admin_user, timezone.now())

            user.balance += claim.summa
            user.save(update_fields=['balance'])

            ChallengeService.update_challenge_progress(user)

            BonusService._clear_user_balance_cache(user.id)

            return success_response({'status': 'approved'})

    @staticmethod
    def reject_claim(claim_id: int, admin_user: User, reason: str):
        with transaction.atomic():
            claim = BonusRepo.get_pending_claim(claim_id)
            if not claim:
                return error_response(ResultCodes.CLAIM_NOT_FOUND)

            user = claim.user
            BonusRepo.reject(claim, admin_user, reason, timezone.now())

            BonusService._clear_user_balance_cache(user.id)

            return success_response({'status': 'rejected'})

    @staticmethod
    def get_user_pending_balance(user: User):
        cache_key = BonusService.PENDING_BALANCE_CACHE_KEY.format(user_id=user.id)
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        value = BonusRepo.sum_pending(user)
        cache.set(cache_key, value, BonusService.CACHE_TIMEOUT)
        return value

    @staticmethod
    def get_user_total_earned(user: User):
        cache_key = BonusService.TOTAL_EARNED_CACHE_KEY.format(user_id=user.id)
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        claims_total = BonusRepo.sum_approved(user)
        challenges_total = ChallengeRepo.sum_completed_reward(user)

        value = claims_total + challenges_total
        cache.set(cache_key, value, BonusService.CACHE_TIMEOUT)
        return value

    @staticmethod
    def get_summary(user: User):
        return success_response({
            'balance': user.balance,
            'pending_balance': BonusService.get_user_pending_balance(user),
            'total_earned': BonusService.get_user_total_earned(user),
        })
