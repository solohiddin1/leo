from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.shared.utils.paginator import CustomPagination
from apps.transaction.api.serializers.bonus_history import UserSummaSerializer
from apps.transaction.repositories.bonus_repo import BonusRepo


class BonusHistoryView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSummaSerializer
    pagination_class = CustomPagination

    def get(self, request):
        claims = BonusRepo.get_claims_for_user(request.user)
        page = self.paginate_queryset(claims)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
