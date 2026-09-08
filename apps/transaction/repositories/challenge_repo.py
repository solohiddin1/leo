from django.db.models import QuerySet, Sum

from apps.transaction.models import Challenge, UserChallengeProgress
from apps.user.models import User


class ChallengeRepo:
    @staticmethod
    def get_visible(now) -> QuerySet[Challenge]:
        return Challenge.objects.filter(is_active=True, end_date__gte=now)

    @staticmethod
    def get_active_for_progress(now) -> QuerySet[Challenge]:
        return Challenge.objects.filter(is_active=True, start_date__lte=now, end_date__gte=now)

    @staticmethod
    def get_or_create_progress(user: User, challenge: Challenge) -> tuple[UserChallengeProgress, bool]:
        return UserChallengeProgress.objects.get_or_create(user=user, challenge=challenge)

    @staticmethod
    def complete_progress(progress: UserChallengeProgress, now) -> None:
        progress.is_completed = True
        progress.completed_at = now

    @staticmethod
    def save_progress(progress: UserChallengeProgress) -> None:
        progress.save()

    @staticmethod
    def sum_completed_reward(user: User) -> int:
        result = UserChallengeProgress.objects.filter(user=user, is_completed=True).aggregate(
            total=Sum('challenge__reward_amount')
        )
        return result['total'] or 0
