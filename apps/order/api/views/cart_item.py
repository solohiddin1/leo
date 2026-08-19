from rest_framework.generics import GenericAPIView

from apps.order.api.serializers.cart import AddToCartSerializer, UpdateCartItemSerializer
from apps.order.services.cart_service import CartService
from apps.shared.permission.client import ClientPermission


class CartItemAddView(GenericAPIView):
    serializer_class = AddToCartSerializer
    permission_classes = [ClientPermission]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return CartService.add_to_cart(
            user=request.user,
            product_id=serializer.validated_data["product_id"],
            quantity=serializer.validated_data["quantity"],
        )


class CartItemView(GenericAPIView):
    serializer_class = UpdateCartItemSerializer
    permission_classes = [ClientPermission]

    def patch(self, request, item_id: int, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return CartService.update_cart_item(
            user=request.user,
            item_id=item_id,
            quantity=serializer.validated_data["quantity"],
        )

    def delete(self, request, item_id: int, *args, **kwargs):
        return CartService.remove_from_cart(request.user, item_id)
