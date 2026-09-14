from django.db.models import QuerySet

from apps.shared.models import TrainingVideo


class TrainingVideoRepo:
    @staticmethod
    def get_active_list() -> QuerySet[TrainingVideo]:
        return TrainingVideo.objects.filter(is_active=True)

    @staticmethod
    def get_by_id(video_id: int) -> TrainingVideo | None:
        return TrainingVideo.objects.filter(id=video_id, is_active=True).first()
