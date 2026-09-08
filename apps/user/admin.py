from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from apps.user.models import Device, Job, Otp, TelegramLoginToken, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email")
    exclude = ('password',)

@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "phone_number", "created_at", "expires_at")


@admin.register(TelegramLoginToken)
class TelegramLoginTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "status", "created_at", "updated_at")


@admin.register(Job)
class JobAdmin(TabbedTranslationAdmin):
    list_display = ("id", "title")


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "device_type", "is_active", "created_at")
    list_filter = ("device_type", "is_active")
