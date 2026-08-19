from django.db.models import QuerySet

from apps.product.models import Product


class ProductRepo:
    @staticmethod
    def get_active_list(subcategory_id: int | None = None) -> QuerySet[Product]:
        if subcategory_id is not None:
            return Product.objects.filter(is_active=True, category_id=subcategory_id)\
                .select_related("category", "category__category")\
                .order_by("-created_at")
        return Product.objects.filter(is_active=True)\
            .select_related("category", "category__category")\
            .order_by("-created_at")

    @staticmethod
    def get_by_id(product_id: int) -> Product | None:
        return (
            Product.objects.filter(pk=product_id, is_active=True)
            .select_related("category", "category__category")
            .first()
        )
