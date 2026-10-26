from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.parsers import MultiPartParser

from apps.shared.permission.client import ClientPermission
from apps.shared.security import GeneralUserThrottle
from apps.shared.utils.result_codes import ResultCodes
from apps.shared.utils.utils import error_response, success_response
from apps.user.api.serializers.profile import UserProfileImageUpdateSerializer
from apps.user.models import User


class UserUpdateProfileImage(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [ClientPermission]
    serializer_class = UserProfileImageUpdateSerializer
    parser_classes = [MultiPartParser]
    throttle_classes = [GeneralUserThrottle]
    http_method_names = ["patch"]

    @extend_schema(
        tags=["user"],
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "avatar": {"type": "string", "format": "binary"}
                },
            }
        }
    )
    def patch(self, request, *args, **kwargs):
        user = request.user
        avatar = request.FILES.get("avatar")
        if avatar and avatar.size > 10 * 1024 * 1024:
            return error_response(
                result=ResultCodes.INVALID_INPUT,
                message={
                    "uz": "Rasm hajmi 10 MB dan oshmasligi kerak.",
                    "ru": "Размер изображения не должен превышать 10 МБ.",
                    "en": "Image size cannot exceed 10 MB.",
                },
            )

        serializer = UserProfileImageUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return success_response({"message": "Image updated"})

        return error_response(ResultCodes.UNKNOWN_ERROR)
