from django.conf import settings
from django.db import models

from apps.product.models import Product
from apps.shared.models import Filial
from apps.user.models import BaseModel, User


class Order(BaseModel):
    total_price = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    filial = models.ForeignKey(Filial, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    new_column = models.BigIntegerField(default=0)

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.BigIntegerField(default=0)
    quantity = models.BigIntegerField(default=1)
    new_column = models.BigIntegerField(default=0)

    def __str__(self):
        return f"OrderItem #{self.pk}"