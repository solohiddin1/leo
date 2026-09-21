from apps.shared.models import Store


class StoreRepo:
    @staticmethod
    def get_by_id(shop_id: int) -> Store | None:
        return Store.objects.filter(shop_id=shop_id).first()
