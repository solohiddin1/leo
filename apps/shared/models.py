from django.db import models

from apps.user.models import BaseModel


class Region(BaseModel):
    soato_id = models.IntegerField(unique=True, null=True)
    name_uz = models.CharField(max_length=100, null=True)
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name_uz


class Filial(BaseModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='filials')
    phone_number = models.CharField(max_length=20, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name