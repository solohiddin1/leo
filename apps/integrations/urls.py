from django.urls import path

from apps.integrations.views import (
    BonusCheckView,
    BonusRedeemView,
    CartDetailView,
    CartItemAddView,
    CartItemView,
    OrderConfirmView,
    OrderCreateView,
    OrderListView,
    UserProvisionView,
)

urlpatterns = [
    path("user/provision/", UserProvisionView.as_view(), name="internal-user-provision"),
    path("bonus/check/", BonusCheckView.as_view(), name="internal-bonus-check"),
    path("bonus/redeem/", BonusRedeemView.as_view(), name="internal-bonus-redeem"),
    path("cart/", CartDetailView.as_view(), name="internal-cart-detail"),
    path("cart/items/", CartItemAddView.as_view(), name="internal-cart-item-add"),
    path("cart/items/<int:item_id>/", CartItemView.as_view(), name="internal-cart-item"),
    path("order/create/", OrderCreateView.as_view(), name="internal-order-create"),
    path("order/confirm/", OrderConfirmView.as_view(), name="internal-order-confirm"),
    path("order/list/", OrderListView.as_view(), name="internal-order-list"),
]
