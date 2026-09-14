from django.urls import path

from apps.shared.api.views.app_info import GetAppInfoAPIView
from apps.shared.api.views.banner import GetBannerListAPIView
from apps.shared.api.views.regions import GetRegionsAPIView

urlpatterns = [
    path("regions/", GetRegionsAPIView.as_view(), name="regions"),
    path("banners/", GetBannerListAPIView.as_view(), name="banner-list"),
    path("app-info/", GetAppInfoAPIView.as_view(), name="app-info"),
]
