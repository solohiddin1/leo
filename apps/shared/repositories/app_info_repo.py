from django.db.models import QuerySet

from apps.shared.models import AppInfo, FAQ


class AppInfoRepo:
    @staticmethod
    def get_app_info() -> AppInfo:
        app_info = AppInfo.objects.first()
        if not app_info:
            app_info = AppInfo.objects.create(
                telegram_support_username="@LEO_OFFICE3366",
                call_center_phones=["+998 99 653 33 66"],
                email_support="shoikrom@bk.ru",
                working_hours_uz="Dushanba - Shanba: 09:00 - 18:00",
                working_hours_ru="Понедельник - Суббота: 09:00 - 18:00",
            )
        return app_info


class FAQRepo:
    @staticmethod
    def get_active_faqs() -> QuerySet[FAQ]:
        return FAQ.objects.filter(is_active=True)
