from django.urls import path

from apps.shared.api.views.regions import GetRegionsAPIView

urlpatterns = [
    path('regions/', GetRegionsAPIView.as_view(), name='regions'),
]