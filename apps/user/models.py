from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Avatar(BaseModel):
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to="avatars", null=True, blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser, BaseModel, PermissionsMixin):
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    main_balance = models.FloatField(default=0)
    balance = models.BigIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    otp_sent_count = models.IntegerField(default=0)
    telegram_id = models.CharField(max_length=20, blank=True, null=True)
    telegram_username = models.CharField(max_length=100, blank=True, null=True)
    lang = models.CharField(max_length=5, blank=True, null=True)
    is_developer = models.BooleanField(default=False)

    avatar = models.OneToOneField(
        Avatar,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone_number"]


class Otp(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    code = models.CharField(max_length=4)
    is_verified = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    device_id = models.CharField(max_length=128, blank=True, null=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.code}-{self.phone_number}"

    class Meta:
        indexes = [
            models.Index(fields=["user"])
        ]

class TelegramLoginToken(BaseModel):
    STATUS_CHOICES = (
        ("PENDING", "PENDING"),
        ("CONFIRMED", "CONFIRMED"),
        ("EXPIRED", "EXPIRED"),
    )

    token = models.CharField(max_length=128, unique=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="PENDING")
    telegram_id = models.BigIntegerField(null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tg_login_tokens",
    )
    expires_at = models.DateTimeField()
    otp_mode = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.token[:8]} {self.status}"


class Device(BaseModel):
    DEVICE_TYPE_CHOICES = (
        ("ANDROID", "ANDROID"),
        ("IOS", "IOS"),
        ("WEB", "WEB"),
    )
    name = models.CharField(max_length=128)
    device_type = models.CharField(max_length=16, choices=DEVICE_TYPE_CHOICES, default="WEB")
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_device",
    )
    device_id = models.CharField(max_length=128)
    fcm_token = models.CharField(max_length=128, null=True, blank=True)
    is_active = models.BooleanField(default=True)
