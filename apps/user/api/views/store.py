from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import ListAPIView

from apps.shared.models import Store
from apps.shared.permission.client import ClientPermission
from apps.shared.utils.utils import success_response
from apps.user.api.serializers.store import StoreSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="all_stores",
            type=bool,
            location=OpenApiParameter.QUERY,
            description="Fetch all stores regardless of bonus code claims",
            required=False,
        )
    ]
)
class UserRedeemedStoreListView(ListAPIView):
    permission_classes = [ClientPermission]
    serializer_class = StoreSerializer

    def get_queryset(self):
        all_stores = self.request.query_params.get("all_stores", "").lower() == "true"
        if all_stores:
            return Store.objects.all()

        user_stores = Store.objects.filter(bonus_claims__user=self.request.user).distinct()
        if not user_stores.exists():
            return Store.objects.all()
        return user_stores

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)
