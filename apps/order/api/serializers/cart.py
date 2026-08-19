from rest_framework import serializers

from apps.order.models import Cart, CartItem
from apps.product.api.serializers.products import ProductListSerializer


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1, default=1)


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)


class ItemsSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "price"]


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    items = ItemsSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


    def get_total_price(self, obj):
        total_price = sum(item.price for item in obj.items.all())
        return total_price
