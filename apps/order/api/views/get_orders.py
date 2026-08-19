from rest_framework.generics import GenericAPIView

from apps.order.api.serializers.order import OrderSerializer
from apps.order.services.order_service import OrderService
from apps.shared.permission.client import ClientPermission


class OrdersView(GenericAPIView):
    permission_classes = [ClientPermission]
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        return OrderService.get_orders(request.user, self.request)
