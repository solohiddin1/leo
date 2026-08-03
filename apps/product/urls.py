from django.urls import path

from apps.product.api.views.get_categories import GetCategoriesApiView

urlpatterns = [
    path('get_categories/', GetCategoriesApiView.as_view(), name='get_categories'),
]