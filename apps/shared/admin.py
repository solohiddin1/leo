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
    TrainingVideoStatus,
)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "soato_id", "name_uz", "name_ru", "name_en")
    search_fields = ("name_uz", "name_ru", "name_en", "soato_id")


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "shop_id", "name", "region", "phone_number", "address", "lat", "long")
    list_editable = ("shop_id",)
    search_fields = ("name", "shop_id", "address")
    list_filter = ("region",)


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "send_otp_code",
        "otp_wait_seconds",
        "otp_timeout_seconds",
        "training_video_reward_points",
    )


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
    list_display = (
        "id",
        "name_uz",
        "name_ru",
        "user",
        "status",
        "points_awarded",
        "awarded_points",
        "youtube_url",
        "file",
        "ordering",
        "is_active",
        "created_at",
    )
    list_editable = ("ordering", "is_active")
    list_filter = ("status", "points_awarded", "is_active")
    search_fields = (
        "name_uz",
        "name_ru",
        "description_uz",
        "description_ru",
        "user__username",
        "user__first_name",
        "user__last_name",
    )
    actions = ["approve_videos", "reject_videos"]

    @admin.action(description="Tanlangan videolarni tasdiqlash (va ball berish)")
    def approve_videos(self, request, queryset):
        from apps.shared.services.training_video_service import TrainingVideoService

        count, points = TrainingVideoService.approve_videos(queryset)
        self.message_user(
            request,
            f"{count} ta video tasdiqlandi. Foydalanuvchilarga jami {points} ball berildi.",
        )

    @admin.action(description="Tanlangan videolarni rad etish")
    def reject_videos(self, request, queryset):
        updated = queryset.update(status=TrainingVideoStatus.REJECTED)
        self.message_user(request, f"{updated} ta video rad etildi.")

    def save_model(self, request, obj, form, change):
        from apps.shared.services.training_video_service import TrainingVideoService

        super().save_model(request, obj, form, change)
        if obj.status == TrainingVideoStatus.APPROVED and not obj.points_awarded:
            TrainingVideoService.approve_video(obj)
