from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.order.models import Cart, CartItem, Order, OrderItem, OrderProblemImage
from apps.order.services.order_service import OrderService


class OrderProblemImageInline(admin.TabularInline):
    model = OrderProblemImage
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class CartInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "store", "state", "is_completed")
    list_filter = ("state", "is_completed")
    inlines = [OrderItemInline, OrderProblemImageInline]
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


class HasItemsFilter(admin.SimpleListFilter):
    title = "Savat holati"
    parameter_name = "has_items"

    def lookups(self, request, model_admin):
        return [
            ("yes", "Mahsulot bor (Non-empty)"),
            ("no", "Bo'sh (Empty)"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(items__isnull=False).distinct()
        if self.value() == "no":
            return queryset.filter(items__isnull=True)
        return queryset


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "items_count", "total_price", "cart_items_display")
    list_filter = (HasItemsFilter, "items__product")
    inlines = [CartInline]
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "items__product__name",
        "items__product__name_uz",
        "items__product__name_ru",
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("user")
            .prefetch_related("items__product")
        )

    @admin.display(description="Mahsulotlar soni")
    def items_count(self, obj):
        return sum(item.quantity for item in obj.items.all())

    @admin.display(description="Umumiy summa")
    def total_price(self, obj):
        total = sum(item.price * item.quantity for item in obj.items.all())
        return f"{total:,}".replace(",", " ") + " so'm"

    @admin.display(description="Savatdagi mahsulotlar")
    def cart_items_display(self, obj):
        items = list(obj.items.all())
        if not items:
            return "Bo'sh"
        lines = [
            f"• <b>{item.product.name}</b> × {item.quantity} ({(item.price * item.quantity):,} so'm)".replace(
                ",", " "
            )
            for item in items
        ]
        return mark_safe("<br>".join(lines))
