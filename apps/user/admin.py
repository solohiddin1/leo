from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from apps.user.models import Device, Job, Otp, TelegramLoginToken, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "balance")
    search_fields = ("username", "first_name", "last_name", "telegram_id", "telegram_username")
    exclude = ('password',)


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "phone_number", "created_at", "expires_at")
    search_fields = ("user__username", "user__first_name", "user__last_name", "code",
                     "phone_number")


@admin.register(TelegramLoginToken)
class TelegramLoginTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "status", "created_at", "updated_at")
    search_fields = ("user__username", "token")


@admin.register(Job)
class JobAdmin(TabbedTranslationAdmin):
    list_display = ("id", "title")
    search_fields = ("title", "title_uz", "title_ru")


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "device_type", "is_active", "created_at")
    list_filter = ("device_type", "is_active")
    search_fields = ("user__username", "name")
