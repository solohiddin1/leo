from django.urls import path

from apps.notification.api.views.notification_list import NotificationListView
from apps.notification.api.views.notification_read import NotificationReadView

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification_list"),
    path("<int:notification_id>/read/", NotificationReadView.as_view(), name="notification_read"),
    path("read_all/", NotificationReadView.as_view(), name="notifications_read_all"),
]
