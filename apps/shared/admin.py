from django.contrib import admin

from apps.shared.models import Region, Filial, SiteConfig


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'soato_id', 'name_uz', 'name_ru', 'name_en')


@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'phone_number', 'address', 'lat', 'long')
    list_filter = ('region',)


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('send_otp_code', 'otp_wait_seconds', 'otp_timeout_seconds')