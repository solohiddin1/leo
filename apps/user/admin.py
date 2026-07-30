from django.contrib import admin

from apps.user.models import User, Otp, TelegramLoginToken


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'phone_number', 'created_at', 'expires_at')

@admin.register(TelegramLoginToken)
class TelegramLoginTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'status', 'created_at', 'updated_at')