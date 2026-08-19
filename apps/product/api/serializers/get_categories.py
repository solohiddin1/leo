from rest_framework import serializers

from apps.product.models import Category, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name_uz", "name_ru", "category"]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name_uz", "name_ru", "subcategories"]


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = ["id", "name_uz", "name_ru", "category", "product_count"]

    def get_product_count(self, obj) -> int:
        return obj.product_category.count()
