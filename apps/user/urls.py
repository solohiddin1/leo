from django.urls import path
from apps.user.api.views.register import RegisterAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='index'),
]