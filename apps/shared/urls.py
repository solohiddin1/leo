from django.urls import path

from apps.shared.api.views.banner import GetBannerDetailAPIView, GetBannerListAPIView
from apps.shared.api.views.regions import GetRegionsAPIView

urlpatterns = [
    path("regions/", GetRegionsAPIView.as_view(), name="regions"),
    path("banners/", GetBannerListAPIView.as_view(), name="banner-list"),
    path("banners/<int:pk>/", GetBannerDetailAPIView.as_view(), name="banner-detail"),
]
