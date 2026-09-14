from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView

from apps.order.api.serializers.order import OrderConfirmSerializer
from apps.order.services.order_service import OrderService
from apps.shared.permission.client import ClientPermission


class OrderConfirmView(GenericAPIView):
    permission_classes = [ClientPermission]
    serializer_class = OrderConfirmSerializer

    @extend_schema(operation_id="order_confirm")
    def post(self, request, *args, **kwargs):
        return OrderService.confirm_order(request.user, self.request)
