from django.urls import path

from apps.notification.api.views.notification_list import NotificationListView
from apps.notification.api.views.notification_read import NotificationReadView
from apps.notification.api.views.notification_read_all import NotificationReadAllView

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification_list"),
    path("<int:notification_id>/read/", NotificationReadView.as_view(), name="notification_read"),
    path("read_all/", NotificationReadAllView.as_view(), name="notifications_read_all"),
]
