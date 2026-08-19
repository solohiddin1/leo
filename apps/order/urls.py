from django.urls import path

from apps.order.api.views.cart import CartView
from apps.order.api.views.cart_item import CartItemAddView, CartItemView
from apps.order.api.views.create_order import OrderCreateView
from apps.order.api.views.get_orders import OrdersView

urlpatterns = [
    path("cart/", CartView.as_view()),
    path("cart/items/", CartItemAddView.as_view()),
    path("cart/items/<int:item_id>/", CartItemView.as_view()),
    path("order/create_order/", OrderCreateView.as_view()),
    path("order/orders/", OrdersView.as_view()),
]
