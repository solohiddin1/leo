from rest_framework import serializers

from apps.order.models import Order, OrderItem
from apps.product.api.serializers.products import ProductListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'total_price', 'total', 'state', 'is_completed', 'items', 'created_at']


class OrderCreateSerializer(serializers.Serializer):
    cart_item_ids = serializers.ListField(child=serializers.IntegerField(min_value=1), min_length=1)
    store_id = serializers.IntegerField(required=True)
