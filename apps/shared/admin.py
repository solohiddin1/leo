from django.contrib import admin

from apps.product.admin import image_preview
from apps.shared.models import Banner, Region, SiteConfig, Store


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "soato_id", "name_uz", "name_ru", "name_en")


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region", "phone_number", "address", "lat", "long")
    list_filter = ("region",)


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "required_bonus_images_count", "send_otp_code", "otp_wait_seconds", "otp_timeout_seconds")


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "ordering", "is_active", "image_preview")
    list_editable = ("ordering", "is_active")
    readonly_fields = ('image_compressed', )

    image_preview = image_preview
