from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone

from apps.transaction.models import Challenge
from apps.transaction.repositories.bonus_repo import BonusRepo
from apps.transaction.repositories.challenge_repo import ChallengeRepo
from apps.user.models import User


class ChallengeService:
    @staticmethod
    def get_visible_challenges() -> QuerySet[Challenge]:
        return ChallengeRepo.get_visible(timezone.now())

    @staticmethod
    def update_challenge_progress(user: User):
        from apps.transaction.services.bonus_service import BonusService

        now = timezone.now()
        active_challenges = ChallengeRepo.get_active_for_progress(now)

        for challenge in active_challenges:
            progress, _ = ChallengeRepo.get_or_create_progress(user, challenge)
            if not progress.is_completed:
                progress.current_count = BonusRepo.count_approved_claims_for_product(user, challenge.product)
                if progress.current_count >= challenge.target_count:
                    ChallengeRepo.complete_progress(progress, now)
                    # Reward user
                    user.balance += challenge.reward_amount
                    user.save(update_fields=['balance'])
                    transaction.on_commit(
                        lambda user=user, challenge=challenge: ChallengeService._notify_challenge_completed(user, challenge)
                    )
                ChallengeRepo.save_progress(progress)

        # Invalidate cache if any changes made
        BonusService._clear_user_balance_cache(user.id)

    @staticmethod
    def _notify_challenge_completed(user: User, challenge: Challenge) -> None:
        from apps.notification.messages import NotificationMessages
        from apps.notification.services.admin_telegram_service import AdminTelegramNotifier
        from apps.notification.services.notification_service import NotificationService

        msg = NotificationMessages.challenge_completed_msg
        title, body = msg.render(
            user.lang, challenge_title=challenge.title, reward=challenge.reward_amount
        )
        NotificationService.send_to_user(
            user=user,
            title=title,
            body=body,
            notification_type="CHALLENGE",
            data={
                "type": msg.type.value,
                "challenge_id": challenge.id,
                "reward": challenge.reward_amount,
            },
        )

        AdminTelegramNotifier.send(
            f"🏆 {user.username} completed the '{challenge.title}' challenge "
            f"and was awarded {challenge.reward_amount}."
        )
