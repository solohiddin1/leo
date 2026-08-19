from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from apps.product.api.serializers.get_categories import SubCategoryDetailSerializer
from apps.product.models import SubCategory
from apps.shared.security import GeneralThrottle
from apps.shared.utils.utils import success_response


class SubCategoriesApiView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SubCategoryDetailSerializer
    throttle_classes = [GeneralThrottle]
    queryset = SubCategory.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return success_response(serializer.data)
