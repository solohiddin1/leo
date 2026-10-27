from django.db.models import Q, QuerySet

from apps.shared.models import TrainingVideo, TrainingVideoStatus


class TrainingVideoRepo:
    @staticmethod
    def get_active_list(user=None) -> QuerySet[TrainingVideo]:
        qs = TrainingVideo.objects.filter(is_active=True)
        if user and user.is_authenticated:
            qs = qs.filter(Q(status=TrainingVideoStatus.APPROVED) | Q(user=user))
        else:
            qs = qs.filter(status=TrainingVideoStatus.APPROVED)
        return qs

    @staticmethod
    def get_by_id(video_id: int, user=None) -> TrainingVideo | None:
        qs = TrainingVideo.objects.filter(id=video_id, is_active=True)
        if user and user.is_authenticated:
            qs = qs.filter(Q(status=TrainingVideoStatus.APPROVED) | Q(user=user))
        else:
            qs = qs.filter(status=TrainingVideoStatus.APPROVED)
        return qs.first()
