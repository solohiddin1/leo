from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.transaction.api.serializers.shop_lookup import ShopLookupResponseSerializer, ShopLookupSerializer
from apps.transaction.services.shop_service import ShopService


class ShopLookupView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShopLookupSerializer

    @extend_schema(
        responses={200: ShopLookupResponseSerializer},
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return ShopService.lookup_shop(serializer.validated_data['shop_id'])
