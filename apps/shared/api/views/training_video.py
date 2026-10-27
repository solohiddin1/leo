from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny

from apps.shared.api.serializers.training_video import (
    TrainingVideoSerializer,
    TrainingVideoUploadSerializer,
)
from apps.shared.permission.client import ClientPermission
from apps.shared.repositories.training_video_repo import TrainingVideoRepo
from apps.shared.security import GeneralThrottle
from apps.shared.utils.result_codes import ResultCodes
from apps.shared.utils.utils import error_response, success_response


class GetTrainingVideoListAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [GeneralThrottle]
    serializer_class = TrainingVideoSerializer

    @extend_schema(operation_id="shared_training_videos_list")
    def get(self, request, *args, **kwargs):
        user = request.user if request.user and request.user.is_authenticated else None
        videos = TrainingVideoRepo.get_active_list(user=user)
        serializer = self.get_serializer(videos, many=True, context={"request": request})
        return success_response(serializer.data)


class TrainingVideoUploadAPIView(GenericAPIView):
    permission_classes = [ClientPermission]
    throttle_classes = [GeneralThrottle]
    serializer_class = TrainingVideoUploadSerializer
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        operation_id="shared_training_video_upload",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "file": {"type": "string", "format": "binary"},
                    "youtube_url": {"type": "string"},
                },
                "required": ["name"],
            }
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return error_response(
                result=ResultCodes.INVALID_INPUT,
                message={
                    "uz": str(serializer.errors),
                    "ru": str(serializer.errors),
                    "en": str(serializer.errors),
                },
            )
        video = serializer.save()
        return success_response(
            TrainingVideoSerializer(video, context={"request": request}).data,
            status_code=status.HTTP_201_CREATED,
        )
