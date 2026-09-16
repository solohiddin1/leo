from apps.shared.models import Store


class StoreRepo:
    @staticmethod
    def get_by_id(store_id: int) -> Store | None:
        return Store.objects.filter(id=store_id).first()
