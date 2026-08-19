from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from apps.product.api.serializers.products import ProductListSerializer
from apps.product.repositories.product_repo import ProductRepo
from apps.shared.security import GeneralThrottle
from apps.shared.utils.utils import success_response


@extend_schema(parameters=[
    OpenApiParameter(
        name='subcategory',
        type=int,
        location=OpenApiParameter.QUERY,
        description='Filter or page number',
        required=False
    )]
)
class ProductListApiView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductListSerializer
    throttle_classes = [GeneralThrottle]

    def get(self, request, *args, **kwargs):
        subcategory_id = request.query_params.get("subcategory")
        if subcategory_id is not None and not subcategory_id.isdigit():
            subcategory_id = None
        products = ProductRepo.get_active_list(
            subcategory_id=int(subcategory_id) if subcategory_id else None
        )
        serializer = self.get_serializer(products, many=True)
        return success_response(serializer.data)
