from django.db.models import F, Q, Sum, Window
from django.db.models.functions import Coalesce, Rank

from apps.transaction.models import BonusClaimStatus
from apps.user.models import User


class LeaderboardRepo:
    @staticmethod
    def get_ranked_users(limit: int) -> list[User]:
        users = User.objects.annotate(
            earned_from_claims=Coalesce(Sum('points__summa', filter=Q(points__status=BonusClaimStatus.APPROVED)), 0),
            earned_from_challenges=Coalesce(
                Sum('challenge_progress__challenge__reward_amount', filter=Q(challenge_progress__is_completed=True)), 0
            ),
            calc_total_earned=F('earned_from_claims') + F('earned_from_challenges'),
            rank=Window(
                expression=Rank(),
                order_by=F('calc_total_earned').desc()
            )
        ).order_by('rank')

        return list(users[:limit])

    @staticmethod
    def count_users_ahead_of(total: int) -> int:
        return User.objects.annotate(
            total=Coalesce(Sum('points__summa', filter=Q(points__status=BonusClaimStatus.APPROVED)), 0) +
                  Coalesce(Sum('challenge_progress__challenge__reward_amount', filter=Q(challenge_progress__is_completed=True)), 0)
        ).filter(total__gt=total).count()
