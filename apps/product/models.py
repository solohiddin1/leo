from django.db import models

from apps.user.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SubCategory(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.BigIntegerField(default=0)
    bonus_price = models.BigIntegerField(default=0)
    new_column = models.BigIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    def __str__(self):
        return self.name