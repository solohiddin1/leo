from rest_framework.generics import GenericAPIView

from apps.order.api.serializers.order import OrderCreateSerializer
from apps.order.services.order_service import OrderService
from apps.shared.permission.client import ClientPermission


class OrderCreateView(GenericAPIView):
    permission_classes = [ClientPermission]
    serializer_class = OrderCreateSerializer

    def post(self, request, *args, **kwargs):
        return OrderService.create_order(request.user, self.request)
