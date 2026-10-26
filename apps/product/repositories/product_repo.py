from django.db.models import BooleanField, Case, QuerySet, Value, When

from apps.product.models import Product


class ProductRepo:
    @staticmethod
    def get_active_list(subcategory_id: int | None = None) -> QuerySet[Product]:
        qs = Product.objects.all()\
            .annotate(
                is_available=Case(
                    When(is_active=True, price__gt=0, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )\
            .select_related("category", "category__category")\
            .prefetch_related("images", "bonuses")\
            .order_by("-is_available", "-created_at")
        if subcategory_id is not None:
            qs = qs.filter(category_id=subcategory_id)
        return qs

    @staticmethod
    def get_affordable_list(balance: int, subcategory_id: int | None = None) -> QuerySet[Product]:
        qs = Product.objects.filter(
            price__lte=balance,
        ).annotate(
            is_available=Case(
                When(is_active=True, price__gt=0, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        ).select_related("category", "category__category") \
            .prefetch_related("images", "bonuses") \
            .order_by("-is_available", "price")
        if subcategory_id is not None:
            qs = qs.filter(category_id=subcategory_id)
        return qs

    @staticmethod
    def get_by_id(product_id: int) -> Product | None:
        return (
            Product.objects.filter(pk=product_id)
            .select_related("category", "category__category")
            .prefetch_related("images", "bonuses")
            .first()
        )
