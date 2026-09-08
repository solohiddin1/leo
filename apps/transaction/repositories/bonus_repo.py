from django.db.models import QuerySet, Sum

from apps.transaction.models import Bonus, BonusClaimStatus, BonusCode, UserSumma, UserSummaImage
from apps.user.models import User


class BonusRepo:
    @staticmethod
    def get_by_code(code: str) -> BonusCode | None:
        return BonusCode.objects.select_related('bonus').filter(code=code).first()

    @staticmethod
    def lock_by_code(code: str) -> BonusCode | None:
        return BonusCode.objects.select_related('bonus').select_for_update().filter(code=code).first()

    @staticmethod
    def mark_used(bonus_code: BonusCode) -> None:
        bonus_code.is_used = True
        bonus_code.save(update_fields=['is_used'])

    @staticmethod
    def create_claim(user: User, bonus: Bonus, code: BonusCode, store_id: int) -> UserSumma:
        return UserSumma.objects.create(
            user=user,
            bonus=bonus,
            code=code,
            store_id=store_id,
            product=bonus.product,
            summa=bonus.summa,
        )

    @staticmethod
    def bulk_create_images(user_summa: UserSumma, images) -> None:
        UserSummaImage.objects.bulk_create([
            UserSummaImage(user_summa=user_summa, image=img) for img in images
        ])

    @staticmethod
    def get_claims_for_user(user: User) -> QuerySet[UserSumma]:
        return UserSumma.objects.filter(user=user).order_by('-created_at')

    @staticmethod
    def get_pending_claim(claim_id: int) -> UserSumma | None:
        return UserSumma.objects.select_for_update().filter(id=claim_id, status=BonusClaimStatus.PENDING).first()

    @staticmethod
    def approve(claim: UserSumma, admin_user: User, now) -> None:
        claim.status = BonusClaimStatus.APPROVED
        claim.reviewed_by = admin_user
        claim.reviewed_at = now
        claim.save()

    @staticmethod
    def reject(claim: UserSumma, admin_user: User, reason: str, now) -> None:
        claim.status = BonusClaimStatus.REJECTED
        claim.rejection_reason = reason
        claim.reviewed_by = admin_user
        claim.reviewed_at = now
        claim.save()

    @staticmethod
    def sum_pending(user: User) -> int:
        result = UserSumma.objects.filter(user=user, status=BonusClaimStatus.PENDING).aggregate(total=Sum('summa'))
        return result['total'] or 0

    @staticmethod
    def sum_approved(user: User) -> int:
        result = UserSumma.objects.filter(user=user, status=BonusClaimStatus.APPROVED).aggregate(total=Sum('summa'))
        return result['total'] or 0

    @staticmethod
    def count_approved_claims_for_product(user: User, product) -> int:
        return UserSumma.objects.filter(user=user, status=BonusClaimStatus.APPROVED, product=product).count()
