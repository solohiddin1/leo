from django.db import models

from apps.user.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="categories/", null=True, blank=True)
    image_compressed = models.ImageField(upload_to="categories/compressed/", null=True, blank=True)

    def __str__(self):
        return self.name


class SubCategory(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="subcategories", blank=True, null=True
    )
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to="subcategories/", null=True, blank=True)
    image_compressed = models.ImageField(upload_to="subcategories/compressed/",
                                         null=True, blank=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.BigIntegerField(default=0)
    bonus_price = models.BigIntegerField(default=0)
    new_column = models.BigIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="product_category",
    )

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", null=True)
    image = models.ImageField(upload_to="images/")
    image_compressed = models.ImageField(upload_to="images/compressed/", null=True, blank=True)

    def __str__(self):
        return f"{self.image}"
