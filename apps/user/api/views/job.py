from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from apps.shared.security import GeneralThrottle
from apps.shared.utils.utils import success_response
from apps.user.api.serializers.job import JobSerializer
from apps.user.services.job_service import JobService


class JobsAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [GeneralThrottle]
    serializer_class = JobSerializer

    def get(self, request, *args, **kwargs):
        jobs = JobService.get_all_jobs()
        serializer = self.get_serializer(jobs, many=True)
        return success_response(serializer.data)