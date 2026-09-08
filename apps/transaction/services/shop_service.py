from apps.shared.repositories.store_repo import StoreRepo
from apps.shared.utils.result_codes import ResultCodes
from apps.shared.utils.utils import error_response, success_response


class ShopService:
    @staticmethod
    def lookup_shop(shop_id: int):
        store = StoreRepo.get_by_id(shop_id)
        if not store:
            return error_response(ResultCodes.STORE_NOT_FOUND)

        return success_response({
            'name': store.name,
            'is_priority': store.is_priority,
            'bonus_boost_percentage': store.bonus_boost_percentage
        })
