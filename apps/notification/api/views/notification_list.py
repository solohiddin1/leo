from rest_framework.generics import GenericAPIView

from apps.notification.api.serializers.notification import NotificationSerializer
from apps.notification.repositories.notification_repo import NotificationRepo
from apps.shared.permission.client import ClientPermission
from apps.shared.utils.paginator import CustomPagination


class NotificationListView(GenericAPIView):
    permission_classes = [ClientPermission]
    serializer_class = NotificationSerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        notifications = NotificationRepo.get_user_notifications(request.user)
        page = self.paginate_queryset(notifications)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
