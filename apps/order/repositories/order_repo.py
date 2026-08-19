from django.db import transaction
from django.db.models import QuerySet

from apps.order.models import Cart, Order, OrderItem
from apps.user.models import User


class OrderRepo:
    @staticmethod
    def get_user_orders(user: User) -> QuerySet[Order]:
        return Order.objects.filter(user=user).order_by("-created_at")

    @staticmethod
    def get_order_by_id(user: User, order_id: int) -> Order | None:
        return Order.objects.filter(user=user, id=order_id).first()

    @staticmethod
    @transaction.atomic
    def create_order_from_cart(user: User, cart: Cart) -> Order | None:
        cart_items = cart.items.select_related("product").all()
        if not cart_items.exists():
            return None

        total_price = sum(item.price for item in cart_items)
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            total=total_price  # total seems to be redundant or used differently
        )

        order_items = [
            OrderItem(
                order=order,
                user=user,
                product=item.product,
                price=item.price,
                quantity=item.quantity
            )
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)

        cart.items.all().delete()

        return order
