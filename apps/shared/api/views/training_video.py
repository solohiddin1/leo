from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from apps.shared.api.serializers.training_video import TrainingVideoSerializer
from apps.shared.repositories.training_video_repo import TrainingVideoRepo
from apps.shared.security import GeneralThrottle
from apps.shared.utils.utils import success_response


class GetTrainingVideoListAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [GeneralThrottle]
    serializer_class = TrainingVideoSerializer

    @extend_schema(operation_id="shared_training_videos_list")
    def get(self, request, *args, **kwargs):
        videos = TrainingVideoRepo.get_active_list()
        serializer = self.get_serializer(videos, many=True)
        return success_response(serializer.data)
