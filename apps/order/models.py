from django.conf import settings
from django.db import models

from apps.product.models import Product
from apps.shared.models import Store
from apps.user.models import BaseModel, User


class OrderState(models.TextChoices):
    CHECKING = "checking", "Checking"
    ACCEPTED = "accepted", "Accepted"
    ON_WAY = "on_way", "On Way"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class Order(BaseModel):
    total_price = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    store = models.ForeignKey(
        Store, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders"
    )
    total = models.IntegerField(default=1, verbose_name="общая сумма")
    is_completed = models.BooleanField(default=False)
    state = models.CharField(
        max_length=20,
        choices=OrderState.choices,
        default=OrderState.CHECKING,
    )

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    price = models.BigIntegerField(default=0)
    quantity = models.BigIntegerField(default=1)

    def __str__(self):
        return f"OrderItem #{self.pk}"


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_cart")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_carts"
    )
    quantity = models.BigIntegerField(default=1)
    price = models.BigIntegerField(default=0)

    class Meta:
        unique_together = ("cart", "product")
