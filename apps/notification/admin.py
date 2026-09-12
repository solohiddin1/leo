from django.contrib import admin

from apps.notification.models import MarketingNotification, Notification, NotificationLog
from apps.notification.services.marketing_notification_service import (
    MarketingNotificationService,
)


@admin.register(MarketingNotification)
class MarketingNotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "audience",
        "status",
        "total_targets",
        "sent_count",
        "failed_count",
        "sent_at",
        "created_at",
    )
    list_filter = ("status", "audience")
    search_fields = ("title", "body")
    readonly_fields = (
        "status",
        "total_targets",
        "sent_count",
        "failed_count",
        "sent_at",
        "created_by",
    )
    actions = ["send_notifications"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.action(description="Send selected marketing notifications")
    def send_notifications(self, request, queryset):
        sent = 0
        # for marketing_notification in queryset.filter(status="DRAFT"):
        for marketing_notification in queryset.filter():
            MarketingNotificationService.send(marketing_notification)
        sent += 1
        self.message_user(request, f"Sent {sent} marketing notification(s).")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "notification_type", "is_read", "created_at")
    list_filter = ("notification_type", "is_read")
    search_fields = ("title", "user__username")

    def has_add_permission(self, request):
        return False


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "device", "status", "fcm_message_id", "created_at")
    list_filter = ("status",)

    def has_add_permission(self, request):
        return False
