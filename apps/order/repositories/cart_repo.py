from apps.order.models import Cart
from apps.user.models import User

class CartRepo:
    @staticmethod
    def get_or_create_cart(user: User) -> Cart:
        cart, created = Cart.objects.get_or_create(user=user)
        return cart
