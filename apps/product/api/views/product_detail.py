from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from apps.product.api.serializers.products import ProductDetailSerializer
from apps.product.repositories.product_repo import ProductRepo
from apps.shared.security import GeneralThrottle
from apps.shared.utils.result_codes import ResultCodes
from apps.shared.utils.utils import error_response, success_response


class ProductDetailApiView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductDetailSerializer
    throttle_classes = [GeneralThrottle]

    def get(self, request, pk: int, *args, **kwargs):
        product = ProductRepo.get_by_id(pk)
        if not product:
            return error_response(ResultCodes.PRODUCT_NOT_FOUND)
        serializer = self.get_serializer(product)
        return success_response(serializer.data)
