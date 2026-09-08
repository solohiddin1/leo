from django.db.models import QuerySet

from apps.product.models import Product


class ProductRepo:
    @staticmethod
    def get_active_list(subcategory_id: int | None = None) -> QuerySet[Product]:
        qs = Product.objects.filter(is_active=True)\
            .select_related("category", "category__category")\
            .prefetch_related("images", "bonuses")\
            .order_by("-created_at")
        if subcategory_id is not None:
            qs = qs.filter(category_id=subcategory_id)
        return qs

    @staticmethod
    def get_affordable_list(balance: int, subcategory_id: int | None = None) -> QuerySet[Product]:
        qs = Product.objects.filter(
            is_active=True,
            is_bonus_redeemable=True,
            bonus_price__lte=balance,
        ).select_related("category", "category__category") \
            .prefetch_related("images", "bonuses") \
            .order_by("bonus_price")
        if subcategory_id is not None:
            qs = qs.filter(category_id=subcategory_id)
        return qs

    @staticmethod
    def get_by_id(product_id: int) -> Product | None:
        return (
            Product.objects.filter(pk=product_id, is_active=True)
            .select_related("category", "category__category")
            .prefetch_related("images", "bonuses")
            .first()
        )
