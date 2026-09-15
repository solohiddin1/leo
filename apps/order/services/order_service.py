from urllib.request import Request

from apps.order.api.serializers.order import (
    OrderConfirmSerializer,
    OrderCreateSerializer,
    OrderSerializer,
)
from apps.order.models import Order
from apps.order.repositories.cart_repo import CartRepo
from apps.order.repositories.order_repo import OrderRepo
from apps.shared.utils.result_codes import ResultCodes
from apps.shared.utils.utils import error_response, success_response
from apps.user.models import User


class OrderService:
    @staticmethod
    def get_order_detail(user: User, order_id: int, request: Request):
        order = OrderRepo.get_order_by_id(user, order_id)
        if order is None:
            return error_response(ResultCodes.ORDER_NOT_FOUND)
        serialized = OrderSerializer(order, context={'request': request}).data
        return success_response(serialized)

    @staticmethod
    def get_active_confirmable_orders(user: User, request: Request):
        orders = OrderRepo.get_active_orders(user)
        serialized = OrderSerializer(orders, many=True, context={'request': request}).data
        return success_response(serialized)

    @staticmethod
    def create_order(user: User, request: Request):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(ResultCodes.INVALID_INPUT)

        item_ids = serializer.validated_data.get('cart_item_ids', [])
        store_id = serializer.validated_data.get('store_id')

        cart = CartRepo.get_or_create_cart(user)
        cart_items = CartRepo.get_cart_items_by_ids(cart, item_ids)
        if not cart_items.exists():
            return error_response(ResultCodes.CART_ITEM_NOT_FOUND)

        order = OrderRepo.create_order_from_items(user, cart_items, store_id)
        if order is None:
            return error_response(ResultCodes.INSUFFICIENT_BALANCE)

        serialized = OrderSerializer(order, context={'request': request}).data
        return success_response(serialized)

    @staticmethod
    def confirm_order(user: User, request: Request):
        serializer = OrderConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(ResultCodes.INVALID_INPUT)

        order_id = serializer.validated_data['order_id']
        is_good = serializer.validated_data['is_good']
        problem_note = serializer.validated_data.get('problem_note', '')

        images = request.FILES.getlist('images') or request.FILES.getlist('image')
        if not images:
            images = serializer.validated_data.get('images', [])

        if len(images) > 3:
            return error_response(
                result=ResultCodes.INVALID_INPUT,
                message={
                    "uz": "Maksimal 3 ta rasm yuklash mumkin.",
                    "ru": "Разрешено максимум 3 изображения.",
                    "en": "Maximum 3 images allowed.",
                },
            )

        for img in images:
            if img.size > 10 * 1024 * 1024:
                return error_response(
                    result=ResultCodes.INVALID_INPUT,
                    message={
                        "uz": f"Rasm hajmi 10 MB dan oshmasligi kerak.",
                        "ru": f"Размер изображения не должен превышать 10 МБ.",
                        "en": f"Image size cannot exceed 10 MB.",
                    },
                )

        order = OrderRepo.get_order_by_id(user, order_id)
        if order is None:
            return error_response(ResultCodes.ORDER_NOT_FOUND)

        if is_good:
            order = OrderRepo.complete_order(order)
            message = "Order marked as completed."
        else:
            order = OrderRepo.report_order_problem(order, problem_note, images=images)
            message = "Order problem reported to admin bot."

        serialized = OrderSerializer(order, context={'request': request}).data
        return success_response({'order': serialized, 'message': message})

    @staticmethod
    def approve_order(order: Order) -> Order:
        return OrderRepo.approve_order(order)

    @staticmethod
    def reject_order(order: Order) -> Order:
        return OrderRepo.reject_order(order)
