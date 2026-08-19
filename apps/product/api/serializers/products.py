from rest_framework import serializers

from apps.product.models import Image, Product, SubCategory


class ProductSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name_uz", "name_ru"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(read_only=True, many=True)
    category = ProductSubCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name_uz",
            "name_ru",
            "price",
            "bonus_price",
            "images",
            "category",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(read_only=True, many=True)
    category = ProductSubCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name_uz",
            "name_ru",
            "description_uz",
            "description_ru",
            "price",
            "bonus_price",
            "new_column",
            "images",
            "category",
            "created_at",
        ]
