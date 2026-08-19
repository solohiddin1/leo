from django.urls import path

from apps.transaction.api.views import CheckCodeView

urlpatterns = [
    path('bonus/', CheckCodeView.as_view(), name='bonus-check'),
]
