from urllib.request import Request

from apps.order.api.serializers.order import OrderSerializer
from apps.order.repositories.cart_repo import CartRepo
from apps.order.repositories.order_repo import OrderRepo
from apps.shared.utils.result_codes import ResultCodes
from apps.shared.utils.utils import error_response, success_response
from apps.user.models import User


class OrderService:
    @staticmethod
    def get_orders(user: User, request: Request):
        orders = OrderRepo.get_user_orders(user)
        serialized = OrderSerializer(orders, many=True, context={'request': request}).data
        return success_response(serialized)

    @staticmethod
    def get_order_detail(user: User, order_id: int, request: Request):
        order = OrderRepo.get_order_by_id(user, order_id)
        if order is None:
            return error_response(ResultCodes.ORDER_NOT_FOUND)
        serialized = OrderSerializer(order, context={'request': request}).data
        return success_response(serialized)

    @staticmethod
    def create_order(user: User, request: Request):
        cart_id = request.data.get('cart_item_id')
        cart = CartRepo.get_cart_by_id(cart_id, request.user)
        if cart is None:
            return error_response(ResultCodes.CART_NOT_FOUND)
        order = OrderRepo.create_order_from_cart(user, cart)
        if order is None:
            return error_response(ResultCodes.CART_EMPTY)

        serialized = OrderSerializer(order, context={'request': request}).data
        return success_response(serialized)
