from rest_framework import serializers

from apps.order.models import Cart, CartItem
from apps.product.api.serializers.products import ProductListSerializer


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1, default=1)
    use_bonus = serializers.BooleanField(default=False)


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)


class ItemsSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "price", "bonus_price", "use_bonus"]


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    user_balance = serializers.SerializerMethodField()
    items = ItemsSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'user_balance']

    def get_total_price(self, obj):
        return sum(
            item.bonus_price * item.quantity if item.use_bonus else item.price * item.quantity
            for item in obj.items.all()
        )

    def get_user_balance(self, obj):
        return obj.user.balance
