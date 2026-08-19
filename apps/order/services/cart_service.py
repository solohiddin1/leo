from urllib.request import Request

from apps.order.api.serializers.cart import CartSerializer
from apps.order.repositories.cart_repo import CartRepo
from apps.product.repositories.product_repo import ProductRepo
from apps.shared.utils.result_codes import ResultCodes
from apps.shared.utils.utils import error_response, success_response
from apps.user.models import User


class CartService:
    @staticmethod
    def get_cart(user: User, request: Request):
        cart = CartRepo.get_or_create_cart(user)
        serialized = CartSerializer(cart, context={'request': request}).data
        return success_response(serialized)

    @staticmethod
    def add_to_cart(user: User, product_id: int, quantity: int):
        quantity = max(quantity, 1)
        product = ProductRepo.get_by_id(product_id)
        if product is None:
            return error_response(ResultCodes.PRODUCT_NOT_FOUND)
        cart = CartRepo.get_or_create_cart(user)
        CartRepo.add_item(cart, product, quantity)
        return success_response(ResultCodes.SUCCESS)

    @staticmethod
    def update_cart_item(user: User, item_id: int, quantity: int):
        quantity = max(quantity, 1)
        cart = CartRepo.get_or_create_cart(user)
        item = CartRepo.get_cart_item_by_id(cart, item_id)
        if item is None:
            return error_response(ResultCodes.CART_ITEM_NOT_FOUND)
        CartRepo.update_item(item, quantity)
        return success_response(ResultCodes.SUCCESS)

    @staticmethod
    def remove_from_cart(user: User, item_id: int):
        cart = CartRepo.get_or_create_cart(user)
        item = CartRepo.get_cart_item_by_id(cart, item_id)
        if item is None:
            return error_response(ResultCodes.CART_ITEM_NOT_FOUND)
        CartRepo.remove_item(item)
        return success_response(ResultCodes.SUCCESS)

    @staticmethod
    def clear_cart(user: User):
        cart = CartRepo.get_or_create_cart(user)
        CartRepo.clear_cart(cart)
        return success_response(ResultCodes.SUCCESS)
