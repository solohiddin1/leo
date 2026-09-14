from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from apps.order.api.serializers.order import OrderConfirmSerializer, OrderSerializer
from apps.order.services.order_service import OrderService
from apps.shared.permission.client import ClientPermission


class OrderConfirmView(GenericAPIView):
    permission_classes = [ClientPermission]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = OrderConfirmSerializer

    @extend_schema(operation_id="order_confirm_list", responses=OrderSerializer(many=True))
    def get(self, request, *args, **kwargs):
        return OrderService.get_active_confirmable_orders(request.user, self.request)

    @extend_schema(
        operation_id="order_confirm",
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'order_id': {'type': 'integer'},
                    'is_good': {'type': 'boolean'},
                    'problem_note': {'type': 'string'},
                    'images': {
                        'type': 'array',
                        'items': {'type': 'string', 'format': 'binary'},
                    },
                },
                'required': ['order_id', 'is_good'],
            }
        },
    )
    def post(self, request, *args, **kwargs):
        return OrderService.confirm_order(request.user, self.request)
