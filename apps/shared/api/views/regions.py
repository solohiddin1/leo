from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from apps.shared.models import Region
from apps.shared.security import GeneralThrottle
from apps.shared.utils.utils import success_response
from apps.user.api.serializers.region import RegionSerializer


class GetRegionsAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [GeneralThrottle]
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def get(self, request, *args, **kwargs):
        regions = self.queryset.all()
        serializer = self.get_serializer(regions, many=True)
        return success_response(serializer.data)