from rest_framework.generics import GenericAPIView

from apps.order.api.serializers.cart import CartSerializer
from apps.order.services.cart_service import CartService
from apps.shared.permission.client import ClientPermission


class CartView(GenericAPIView):
    permission_classes = [ClientPermission]
    serializer_class = CartSerializer

    def get(self, request, *args, **kwargs):
        return CartService.get_cart(request.user, self.request)

    def delete(self, request, *args, **kwargs):
        return CartService.clear_cart(request.user)
