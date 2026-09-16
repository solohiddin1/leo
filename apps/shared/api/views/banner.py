from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from apps.shared.api.serializers.banner import BannerSerializer
from apps.shared.repositories.banner_repo import BannerRepo
from apps.shared.security import GeneralThrottle
from apps.shared.utils.utils import success_response


class GetBannerListAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [GeneralThrottle]
    serializer_class = BannerSerializer

    @extend_schema(operation_id="shared_banners_list")
    def get(self, request, *args, **kwargs):
        banners = BannerRepo.get_active_list()
        serializer = self.get_serializer(banners, many=True)
        return success_response(serializer.data)
