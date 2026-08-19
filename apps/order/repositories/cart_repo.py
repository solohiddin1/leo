from django.db.models import QuerySet

from apps.order.models import Cart, CartItem
from apps.product.models import Product
from apps.user.models import User


class CartRepo:
    @staticmethod
    def get_cart_by_id(cart_id: int, user: User) -> Cart | None:
        cart = Cart.objects.filter(id=cart_id, user=user).first()
        return cart

    @staticmethod
    def get_or_create_cart(user: User) -> Cart:
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    @staticmethod
    def get_cart_items(cart: Cart) -> QuerySet[CartItem]:
        return cart.items.select_related("product").all()

    @staticmethod
    def get_cart_item(cart: Cart, product_id: int) -> CartItem | None:
        return cart.items.filter(product_id=product_id).first()

    @staticmethod
    def get_cart_item_by_id(cart: Cart, item_id: int) -> CartItem | None:
        return cart.items.filter(id=item_id).first()

    @staticmethod
    def add_item(cart: Cart, product: Product, quantity: int) -> CartItem:
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity, "price": product.price * quantity},
        )
        if not created:
            item.quantity += quantity
            item.price = product.price * item.quantity
            item.save(update_fields=["quantity", "price"])
        return item

    @staticmethod
    def update_item(cart_item: CartItem, quantity: int) -> CartItem:
        cart_item.quantity = quantity
        cart_item.price = cart_item.product.price * quantity
        cart_item.save(update_fields=["quantity", "price"])
        return cart_item

    @staticmethod
    def remove_item(cart_item: CartItem) -> None:
        cart_item.delete()

    @staticmethod
    def clear_cart(cart: Cart) -> None:
        cart.items.all().delete()
