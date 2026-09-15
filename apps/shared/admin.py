from django.contrib import admin

from apps.product.admin import image_preview
from apps.product.translation import CustomAdmin
from apps.shared.models import (
    AppInfo,
    Banner,
    FAQ,
    Region,
    SiteConfig,
    Store,
    TrainingVideo,
)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "soato_id", "name_uz", "name_ru", "name_en")


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region", "phone_number", "address", "lat", "long")
    list_filter = ("region",)


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "send_otp_code", "otp_wait_seconds", "otp_timeout_seconds")


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "ordering", "is_active", "image_preview")
    list_editable = ("ordering", "is_active")
    readonly_fields = ('image_compressed', )

    image_preview = image_preview


@admin.register(AppInfo)
class AppInfoAdmin(CustomAdmin):
    list_display = (
        "id",
        "telegram_support_username",
        "call_center_phones",
        "email_support",
        "working_hours_uz",
        "working_hours_ru",
        "updated_at",
    )


@admin.register(FAQ)
class FAQAdmin(CustomAdmin):
    list_display = ("id", "question_uz", "question_ru", "ordering", "is_active")
    list_editable = ("ordering", "is_active")
    search_fields = ("question_uz", "question_ru", "answer_uz", "answer_ru")


@admin.register(TrainingVideo)
class TrainingVideoAdmin(CustomAdmin):
    list_display = ("id", "name_uz", "name_ru", "youtube_url", "file", "ordering", "is_active")
    list_editable = ("ordering", "is_active")
    search_fields = ("name_uz", "name_ru", "description_uz", "description_ru")
