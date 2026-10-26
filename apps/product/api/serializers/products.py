from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.product.models import Image, Product, SubCategory


class ProductSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name_uz", "name_ru", "image", "image_compressed"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(read_only=True, many=True)
    category = ProductSubCategorySerializer(read_only=True)
    bonus_summa = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name_uz",
            "name_ru",
            "price",
            "bonus_summa",
            "images",
            "category",
            "is_active",
        ]

    @extend_schema_field(serializers.BooleanField)
    def get_is_active(self, obj):
        return bool(obj.is_active and (obj.price or 0) > 0)

    @extend_schema_field(serializers.IntegerField(allow_null=True))
    def get_bonus_summa(self, obj):
        bonuses = list(obj.bonuses.all())
        if bonuses:
            return bonuses[0].summa
        return None


class AffordableProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(read_only=True, many=True)
    category = ProductSubCategorySerializer(read_only=True)
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name_uz",
            "name_ru",
            "price",
            "images",
            "category",
            "is_active",
        ]

    @extend_schema_field(serializers.BooleanField)
    def get_is_active(self, obj):
        return bool(obj.is_active and (obj.price or 0) > 0)


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(read_only=True, many=True)
    category = ProductSubCategorySerializer(read_only=True)
    bonus_summa = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name_uz",
            "name_ru",
            "description_uz",
            "description_ru",
            "price",
            "bonus_summa",
            "images",
            "category",
            "is_active",
            "created_at",
        ]

    @extend_schema_field(serializers.BooleanField)
    def get_is_active(self, obj):
        return bool(obj.is_active and (obj.price or 0) > 0)

    @extend_schema_field(serializers.IntegerField(allow_null=True))
    def get_bonus_summa(self, obj):
        bonuses = list(obj.bonuses.all())
        if bonuses:
            return bonuses[0].summa
        return None
