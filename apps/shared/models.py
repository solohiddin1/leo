from django.db import models

from apps.user.models import BaseModel


class Region(models.Model):
    soato_id = models.IntegerField(unique=True, null=True)
    name_uz = models.CharField(max_length=100, default="")
    name_ru = models.CharField(max_length=100, blank=True, default="")
    name_en = models.CharField(max_length=100, blank=True, default="")
    ordering = models.IntegerField(default=100)

    class Meta:
        ordering = ["ordering"]

    def __str__(self):
        return self.name_uz


class Store(BaseModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500, blank=True)
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True, blank=True, related_name="filials"
    )
    phone_number = models.CharField(max_length=20, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_priority = models.BooleanField(default=False)
    bonus_boost_percentage = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class SiteConfig(BaseModel):
    send_otp_code = models.BooleanField(default=False)
    otp_wait_seconds = models.IntegerField(default=0)
    otp_timeout_seconds = models.IntegerField(default=0)

    def __str__(self):
        return (
            f"{self.send_otp_code}-{self.otp_wait_seconds}-{self.otp_timeout_seconds}"
        )


class Banner(BaseModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="banners/", null=True, blank=True)
    image_compressed = models.ImageField(upload_to="banners/compressed/", null=True, blank=True)
    url = models.CharField(max_length=500, blank=True)
    ordering = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordering"]

    def __str__(self):
        return self.name


def default_call_center_phones():
    return ["+998 99 653 33 66"]


class AppInfo(BaseModel):
    telegram_support_username = models.CharField(
        max_length=255, blank=True, default="@LEO_OFFICE3366"
    )
    call_center_phones = models.JSONField(
        default=default_call_center_phones, blank=True
    )
    email_support = models.CharField(
        max_length=255, blank=True, default="shoikrom@bk.ru"
    )
    working_hours = models.CharField(
        max_length=255, blank=True, default="Dushanba-Shanba, 09:00 - 18:00"
    )

    class Meta:
        verbose_name = "App Info"
        verbose_name_plural = "App Info"

    def __str__(self):
        return f"App Info ({self.pk})"


class FAQ(BaseModel):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    ordering = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordering", "-created_at"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class TrainingVideo(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    youtube_url = models.CharField(max_length=500, blank=True, default="")
    file = models.FileField(upload_to="training_videos/", null=True, blank=True)
    ordering = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordering", "-created_at"]
        verbose_name = "Training Video"
        verbose_name_plural = "Training Videos"

    def __str__(self):
        return self.name

