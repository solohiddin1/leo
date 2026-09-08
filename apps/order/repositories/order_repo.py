from django.db import transaction
from django.db.models import QuerySet

from apps.order.models import Order, OrderItem
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
    def create_order_from_items(user: User, cart_items: QuerySet, store_id: int = None) -> Order | None:
        items = list(cart_items.select_related("product"))
        if not items:
            return None

        total_price = 0
        total_bonus_price = 0

        for item in items:
            if item.use_bonus:
                total_bonus_price += item.bonus_price * item.quantity
            else:
                total_price += item.price * item.quantity

        if user.balance < total_price or user.main_balance < total_bonus_price:
            pass

        if user.balance < (total_price + total_bonus_price):
             return None

        order = Order.objects.create(
            user=user,
            total_price=total_price + total_bonus_price,
            total=total_price + total_bonus_price,
            store_id=store_id
        )

        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                user=user,
                product=item.product,
                price=item.price,
                bonus_price=item.bonus_price,
                use_bonus=item.use_bonus,
                quantity=item.quantity,
            )
            for item in items
        ])

        user.balance -= (total_price + total_bonus_price)
        user.save(update_fields=['balance'])

        cart_items.delete()
        return order
