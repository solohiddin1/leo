from django.db import transaction

from apps.shared.models import SiteConfig, TrainingVideo, TrainingVideoStatus


class TrainingVideoService:
    @staticmethod
    def approve_video(video: TrainingVideo) -> int:
        from apps.notification.messages import NotificationMessages
        from apps.notification.services.notification_service import NotificationService
        from apps.transaction.services.bonus_service import BonusService

        if video.status == TrainingVideoStatus.APPROVED and video.points_awarded:
            return 0

        config = SiteConfig.objects.first()
        points_to_award = config.training_video_reward_points if config else 0

        video.status = TrainingVideoStatus.APPROVED
        points_awarded_now = 0

        if video.user and not video.points_awarded and points_to_award > 0:
            user = video.user
            with transaction.atomic():
                user.balance += points_to_award
                user.save(update_fields=["balance"])
                video.points_awarded = True
                video.awarded_points = points_to_award
                points_awarded_now = points_to_award

            BonusService._clear_user_balance_cache(user.id)

            try:
                msg = NotificationMessages.training_video_approved_msg
                title, body = msg.render(
                    user.lang,
                    video_name=video.name,
                    points=points_to_award,
                )
                NotificationService.send_to_user(
                    user=user,
                    title=title,
                    body=body,
                    notification_type="TRAINING_VIDEO",
                    data={
                        "type": msg.type.value,
                        "video_id": video.id,
                        "points": points_to_award,
                    },
                )
            except Exception:
                pass

        video.save()
        return points_awarded_now

    @staticmethod
    def approve_videos(queryset) -> tuple[int, int]:
        total_points = 0
        total_approved = 0
        for video in queryset:
            pts = TrainingVideoService.approve_video(video)
            total_points += pts
            total_approved += 1
        return total_approved, total_points
