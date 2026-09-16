from apps.transaction.models import BonusClaimStatus
from apps.transaction.repositories.bonus_repo import BonusRepo
from apps.user.models import User


class AnalyticsService:
    @staticmethod
    def get_user_claim_stats(user: User) -> dict:
        claims = BonusRepo.get_claims_for_user(user)

        return {
            'total_operations': claims.count(),
            'approved': claims.filter(status=BonusClaimStatus.APPROVED).count(),
            'pending': claims.filter(status=BonusClaimStatus.PENDING).count(),
            'cancelled': claims.filter(status=BonusClaimStatus.REJECTED).count(),
        }
