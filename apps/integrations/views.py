from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.integrations.permissions import InternalServicePermission
from apps.integrations.services import resolve_telegram_user
from apps.order.services.cart_service import CartService
from apps.order.services.order_service import OrderService
from apps.transaction.services.bonus_service import BonusService
from apps.user.api.serializers.profile import ProfileSerializer


class InternalAPIView(GenericAPIView):
    """Base for every usta-source-facing endpoint: no JWT, a shared secret instead."""

    authentication_classes = []
    permission_classes = [InternalServicePermission]

    def _resolve_user(self, data):
        chat_id = data.get("telegram_chat_id")
        if not chat_id:
            return None, Response(
                {"success": False, "error": "telegram_chat_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = resolve_telegram_user(
            telegram_chat_id=chat_id,
            phone=data.get("phone", ""),
            first_name=data.get("first_name", ""),
            telegram_username=data.get("telegram_username", ""),
            lang=data.get("lang", "uz"),
            region_id=data.get("region_id"),
        )
        return user, None


class UserProvisionView(InternalAPIView):
    def post(self, request, *args, **kwargs):
        user, err = self._resolve_user(request.data)
        if err:
            return err
        return Response({"success": True, "result": ProfileSerializer(user).data})


class BonusCheckView(InternalAPIView):
    def get(self, request, *args, **kwargs):
        return BonusService.check_code(request.query_params.get("code", ""))


class BonusRedeemView(InternalAPIView):
    def post(self, request, *args, **kwargs):
        user, err = self._resolve_user(request.data)
        if err:
            return err
        return BonusService.redeem_bonus_external(user, request.data.get("code", ""))


class CartDetailView(InternalAPIView):
    def post(self, request, *args, **kwargs):
        # GET-shaped read, POST because it needs telegram_chat_id in a body.
        user, err = self._resolve_user(request.data)
        if err:
            return err
        return CartService.get_cart(user, request)


class CartItemAddView(InternalAPIView):
    def post(self, request, *args, **kwargs):
        user, err = self._resolve_user(request.data)
        if err:
            return err
        return CartService.add_to_cart(
            user,
            product_id=request.data.get("product_id"),
            quantity=request.data.get("quantity", 1),
            request=request,
        )


class CartItemView(InternalAPIView):
    def patch(self, request, *args, **kwargs):
        user, err = self._resolve_user(request.data)
        if err:
            return err
        return CartService.update_cart_item(
            user,
            item_id=kwargs["item_id"],
            quantity=request.data.get("quantity", 1),
            request=request,
        )

    def delete(self, request, *args, **kwargs):
        user, err = self._resolve_user(request.data)
        if err:
            return err
        return CartService.remove_from_cart(user, item_id=kwargs["item_id"], request=request)


class OrderCreateView(InternalAPIView):
    def post(self, request, *args, **kwargs):
        user, err = self._resolve_user(request.data)
        if err:
            return err
        return OrderService.create_order(user, request)


class OrderConfirmView(InternalAPIView):
    def post(self, request, *args, **kwargs):
        user, err = self._resolve_user(request.data)
        if err:
            return err
        return OrderService.confirm_order(user, request)


class OrderListView(InternalAPIView):
    def post(self, request, *args, **kwargs):
        user, err = self._resolve_user(request.data)
        if err:
            return err
        return OrderService.get_active_confirmable_orders(user, request)
