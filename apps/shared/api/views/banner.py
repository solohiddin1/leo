from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from apps.shared.api.serializers.banner import BannerSerializer
from apps.shared.repositories.banner_repo import BannerRepo
from apps.shared.security import GeneralThrottle
from apps.shared.utils.result_codes import ResultCodes
from apps.shared.utils.utils import error_response, success_response


class GetBannerListAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [GeneralThrottle]
    serializer_class = BannerSerializer

    def get(self, request, *args, **kwargs):
        banners = BannerRepo.get_active_list()
        serializer = self.get_serializer(banners, many=True)
        return success_response(serializer.data)


class GetBannerDetailAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [GeneralThrottle]
    serializer_class = BannerSerializer

    def get(self, request, pk: int, *args, **kwargs):
        banner = BannerRepo.get_by_id(pk)
        if not banner:
            return error_response(ResultCodes.BANNER_NOT_FOUND)
        serializer = self.get_serializer(banner)
        return success_response(serializer.data)
