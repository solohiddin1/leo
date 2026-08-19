from django.db.models import QuerySet

from apps.shared.models import Banner


class BannerRepo:
    @staticmethod
    def get_active_list() -> QuerySet[Banner]:
        return Banner.objects.filter(is_active=True)

    @staticmethod
    def get_by_id(banner_id: int) -> Banner | None:
        return Banner.objects.filter(id=banner_id, is_active=True).first()