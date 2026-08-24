from django.urls import path

from apps.transaction.api.views import CheckCodeView, RequiredImagesView

urlpatterns = [
    path('bonus/', CheckCodeView.as_view(), name='bonus-check'),
    path('bonus/required-images/', RequiredImagesView.as_view(), name='bonus-required-images'),
]
