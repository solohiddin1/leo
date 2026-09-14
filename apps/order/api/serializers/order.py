from rest_framework import serializers

from apps.order.models import Order, OrderItem, OrderProblemImage
from apps.product.api.serializers.products import ProductListSerializer

MAX_IMAGE_COUNT = 3
MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # 10 mb


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


class OrderProblemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProblemImage
        fields = ['id', 'image']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    problem_images = OrderProblemImageSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'total_price',
            'state',
            'is_completed',
            'problem_note',
            'problem_images',
            'items',
            'created_at',
        ]


class OrderCreateSerializer(serializers.Serializer):
    cart_item_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1), min_length=1
    )
    store_id = serializers.IntegerField(required=True)


class OrderConfirmSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)
    is_good = serializers.BooleanField(
        required=True,
        help_text="True if order received cleanly, False if order has problem",
    )
    problem_note = serializers.CharField(
        required=False, allow_blank=True, default=""
    )
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        default=list,
        # max_length=MAX_IMAGE_COUNT,
        help_text="List of uploaded problem images (max 3 images, max 10MB per image)",
    )
