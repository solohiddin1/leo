from django.contrib import admin

from apps.order.models import Order, OrderItem, OrderProblemImage
from apps.order.services.order_service import OrderService


class OrderProblemImageInline(admin.TabularInline):
    model = OrderProblemImage
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "store", "state", "is_completed")
    list_filter = ("state", "is_completed")
    inlines = [OrderProblemImageInline]
    actions = ["approve_order", "reject_order"]

    @admin.action(description="Tanlanganni tasdiqlash")
    def approve_order(self, request, queryset):
        success_count = 0
        for order in queryset:
            OrderService.approve_order(order)
            success_count += 1
        self.message_user(request, f"{success_count} ta buyurtma muvaffaqiyatli tasdiqlandi.")

    @admin.action(description="Tanlanganni bekor qilish")
    def reject_order(self, request, queryset):
        success_count = 0
        for order in queryset:
            OrderService.reject_order(order)
            success_count += 1
        self.message_user(request, f"{success_count} ta buyurtma bekor qilindi va mablag' qaytarildi.")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "user", "product", "price", "quantity")
