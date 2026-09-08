from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from apps.product.api.serializers.products import AffordableProductSerializer
from apps.product.repositories.product_repo import ProductRepo
from apps.shared.security import GeneralThrottle
from apps.shared.utils.paginator import CustomPagination


@extend_schema(parameters=[
    OpenApiParameter(
        name='subcategory',
        type=int,
        location=OpenApiParameter.QUERY,
        description='Filter by subcategory id',
        required=False
    )]
)
class AffordableProductListApiView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = AffordableProductSerializer
    throttle_classes = [GeneralThrottle]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        subcategory_id = request.query_params.get("subcategory")
        if subcategory_id is not None and not subcategory_id.isdigit():
            subcategory_id = None

        balance = request.user.balance if request.user.is_authenticated else 0
        products = ProductRepo.get_affordable_list(
            balance=balance,
            subcategory_id=int(subcategory_id) if subcategory_id else None,
        )
        page = self.paginate_queryset(products)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
