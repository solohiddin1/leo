from django.urls import path

from apps.product.api.views.get_categories import GetCategoriesApiView
from apps.product.api.views.product_detail import ProductDetailApiView
from apps.product.api.views.products import ProductListApiView
from apps.product.api.views.subcategories import SubCategoriesApiView

urlpatterns = [
    path("get_categories/", GetCategoriesApiView.as_view(), name="get_categories"),
    path("subcategories/", SubCategoriesApiView.as_view(), name="subcategories"),
    path("products/", ProductListApiView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailApiView.as_view(), name="product_detail"),
]
