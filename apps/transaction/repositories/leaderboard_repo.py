from django.db.models import F, OuterRef, Subquery, Sum, Window
from django.db.models.functions import Coalesce, Rank

from apps.transaction.models import BonusClaimStatus, UserChallengeProgress, UserSumma
from apps.user.models import User


class LeaderboardRepo:
    @staticmethod
    def get_ranked_users(limit: int) -> list[User]:
        claims_sum = UserSumma.objects.filter(
            user=OuterRef('pk'),
            status=BonusClaimStatus.APPROVED
        ).values('user').annotate(
            total=Sum('summa')
        ).values('total')

        challenges_sum = UserChallengeProgress.objects.filter(
            user=OuterRef('pk'),
            is_completed=True
        ).values('user').annotate(
            total=Sum('challenge__reward_amount')
        ).values('total')

        users = User.objects.annotate(
            earned_from_claims=Coalesce(Subquery(claims_sum), 0),
            earned_from_challenges=Coalesce(Subquery(challenges_sum), 0),
            calc_total_earned=F('earned_from_claims') + F('earned_from_challenges'),
            rank=Window(
                expression=Rank(),
                order_by=F('calc_total_earned').desc()
            )
        ).order_by('-calc_total_earned', 'id')

        return list(users[:limit])

    @staticmethod
    def count_users_ahead_of(total: int) -> int:
        claims_sum = UserSumma.objects.filter(
            user=OuterRef('pk'),
            status=BonusClaimStatus.APPROVED
        ).values('user').annotate(
            total=Sum('summa')
        ).values('total')

        challenges_sum = UserChallengeProgress.objects.filter(
            user=OuterRef('pk'),
            is_completed=True
        ).values('user').annotate(
            total=Sum('challenge__reward_amount')
        ).values('total')

        return User.objects.annotate(
            total_earned=Coalesce(Subquery(claims_sum), 0) + Coalesce(Subquery(challenges_sum), 0)
        ).filter(total_earned__gt=total).count()

