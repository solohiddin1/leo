from django.db import models

from apps.user.models import BaseModel, Device, User


class MarketingNotification(BaseModel):
    STATUS_CHOICES = (
        ("DRAFT", "DRAFT"),
        ("SENDING", "SENDING"),
        ("SENT", "SENT"),
        ("FAILED", "FAILED"),
    )
    AUDIENCE_CHOICES = (
        ("ALL", "ALL"),
        ("ANDROID", "ANDROID"),
        ("IOS", "IOS"),
        ("WEB", "WEB"),
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to="marketing_notifications", null=True, blank=True)
    data = models.JSONField(default=dict, blank=True)
    audience = models.CharField(max_length=16, choices=AUDIENCE_CHOICES, default="ALL")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="DRAFT")
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_marketing_notifications",
    )
    total_targets = models.PositiveIntegerField(default=0)
    sent_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class Notification(BaseModel):
    NOTIFICATION_TYPE_CHOICES = (
        ("SYSTEM", "SYSTEM"),
        ("ORDER", "ORDER"),
        ("BONUS", "BONUS"),
        ("MARKETING", "MARKETING"),
        ("CHALLENGE", "CHALLENGE"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    body = models.TextField()
    notification_type = models.CharField(
        max_length=16, choices=NOTIFICATION_TYPE_CHOICES, default="SYSTEM"
    )
    data = models.JSONField(default=dict, blank=True)
    image = models.ImageField(upload_to="notifications", null=True, blank=True)
    is_read = models.BooleanField(default=False)
    marketing_notification = models.ForeignKey(
        MarketingNotification,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications",
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "is_read"])]

    def __str__(self) -> str:
        return self.title


class NotificationLog(BaseModel):
    STATUS_CHOICES = (
        ("SUCCESS", "SUCCESS"),
        ("FAILED", "FAILED"),
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="logs",
    )
    marketing_notification = models.ForeignKey(
        MarketingNotification,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="logs",
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="notification_logs"
    )
    device = models.ForeignKey(
        Device, on_delete=models.SET_NULL, null=True, blank=True, related_name="notification_logs"
    )
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    fcm_message_id = models.CharField(max_length=255, blank=True, default="")
    error_message = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status"])]

    def __str__(self) -> str:
        return f"{self.status}-{self.device_id}"
