from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from apps.shared.api.serializers.app_info import AppInfoSerializer
from apps.shared.repositories.app_info_repo import AppInfoRepo
from apps.shared.security import GeneralThrottle
from apps.shared.utils.utils import success_response


# @extend_schema(exclude=True)
class GetAppInfoAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [GeneralThrottle]
    serializer_class = AppInfoSerializer

    @extend_schema(operation_id="shared_app_info")
    def get(self, request, *args, **kwargs):
        app_info = AppInfoRepo.get_app_info()
        serializer = self.get_serializer(app_info)
        return success_response(serializer.data)
