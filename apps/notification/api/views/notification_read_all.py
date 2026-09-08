from rest_framework.generics import GenericAPIView

from apps.notification.models import Notification
from apps.notification.services.notification_service import NotificationService
from apps.shared.permission.client import ClientPermission


class NotificationReadAllView(GenericAPIView):
    permission_classes = [ClientPermission]
    queryset = Notification.objects.all()

    def post(self, request, *args, **kwargs):
        return NotificationService.read_all(request.user)
