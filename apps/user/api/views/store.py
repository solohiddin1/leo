from rest_framework.generics import ListAPIView

from apps.shared.models import Store
from apps.shared.permission.client import ClientPermission
from apps.shared.utils.utils import success_response
from apps.user.api.serializers.store import StoreSerializer


class UserRedeemedStoreListView(ListAPIView):
    permission_classes = [ClientPermission]
    serializer_class = StoreSerializer

    def get_queryset(self):
        return Store.objects.filter(bonus_claims__user=self.request.user).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)
