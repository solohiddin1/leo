from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True

class User(AbstractUser, BaseModel, PermissionsMixin):
    main_balance = models.FloatField(default=0)
    balance = models.BigIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    otp_sent_count = models.IntegerField(default=0)


class Otp(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
