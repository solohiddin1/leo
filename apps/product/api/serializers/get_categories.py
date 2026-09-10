from rest_framework import serializers

from apps.product.models import Category, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name_uz", "name_ru", "category", "image", "image_compressed"]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name_uz", "name_ru", "image", "image_compressed", "subcategories"]


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = ["id", "name_uz", "name_ru", "category", "image", "image_compressed", "product_count"]

    def get_product_count(self, obj) -> int:
        return obj.product_category.count()
