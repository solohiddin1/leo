from rest_framework.generics import GenericAPIView

from apps.order.api.serializers.order import OrderSerializer
from apps.order.repositories.order_repo import OrderRepo
from apps.shared.permission.client import ClientPermission
from apps.shared.utils.paginator import CustomPagination


class OrdersView(GenericAPIView):
    permission_classes = [ClientPermission]
    serializer_class = OrderSerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        orders = OrderRepo.get_user_orders(request.user)
        page = self.paginate_queryset(orders)
        serializer = self.get_serializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
