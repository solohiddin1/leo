from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from apps.shared.security import GeneralThrottle
from apps.shared.utils.utils import success_response
from apps.product.api.serializers.get_categories import CategorySerializer
from apps.product.models import Category


class GetCategoriesApiView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    throttle_classes = [GeneralThrottle]
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return success_response(serializer.data)
