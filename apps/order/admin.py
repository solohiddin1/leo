from django.contrib import admin

from apps.order.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "store", "state")
    list_filter = ("state",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "user", "product", "price", "quantity")
